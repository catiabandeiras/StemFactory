// Module Pattern
// More information: http://toddmotto.com/mastering-the-module-pattern/

var Slem = (function ($) {
    // Prevents certain actions from being taken and throws exceptions
    "use strict";

    // Private functions
    var _init = function () {

        $("#sim-welcome-msg").fadeIn(1000, function () {
            $("#sim-welcome-desc").fadeIn(1000, function () {
                $("#sim-welcome-start-btn-ctn").fadeIn(1000);
            });
        });

        $("#sim-welcome-start-btn").on("click", function () {
            $("#sim-welcome-ctn").fadeOut(1000, function () {
                $("#sim-step1-ctn").fadeIn(1000);
            });

        });
    };

    return {

        // Public variables
        myPublicVar: "",

        // Public functions
        init: _init

    };

})(jQuery);

// Load when ready
$(document).ready(function () {
    Slem.init();
});