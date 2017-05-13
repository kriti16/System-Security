var fs = require("fs");
var system = require("system");
var webpage = require("webpage");

var grading = require("./grading");
var ex4msg = "I Love CS628A!";

var NUM_ITERATIONS = 4;

function make_refimg_ex4(num, prevUser) {
    if (num > NUM_ITERATIONS) {
        phantom.exit();
        return;
    }
    var user = "grader" + num;
    grading.zoobarRegister(user, "password" + num, function () {
        grading.setProfile(ex4msg, function () {
            var page = webpage.create();
            var url = grading.zoobarBase + "users?user=" + encodeURIComponent(prevUser);
            grading.openOrDie(page, url, function () {
                // Wait for the zoobar counter to settle
                setTimeout(function () {
                    grading.derandomize(page);
                    page.render("lab3-tests/answer-4_" + (num - 1) + ".ref.png");
                    page.close();

                    make_refimg_ex4(num + 1, user);
                }, 2000);
            });
        });
    });
}

function main() {
    grading.initUsers(function(auth) {
        phantom.cookies = auth.graderCookies;
        // answer-1.png: as grader, view a blank users page.
        var page = webpage.create();
        grading.openOrDie(page, grading.zoobarBase + "users", function() {
            grading.derandomize(page);
            page.render("lab3-tests/answer-1.ref.png");
            page.close();

            // answer-3.png, answer-chal.png: view the login page.
            phantom.clearCookies();
            page = webpage.create();
            grading.openOrDie(page, grading.zoobarBase + "login", function() {
                grading.derandomize(page);
                page.render("lab3-tests/answer-3.ref.png");
                page.close();
                if (fs.exists("lab3-tests/answer-chal.ref.png"))
                    fs.remove("lab3-tests/answer-chal.ref.png");
                fs.copy("lab3-tests/answer-3.ref.png",
                        "lab3-tests/answer-chal.ref.png");

                phantom.cookies = auth.attackerCookies;
                grading.setProfile(ex4msg, function () {
                    make_refimg_ex4(1, "attacker");
                });
            });
        });
    });
}

main.apply(null, system.args.slice(1));
