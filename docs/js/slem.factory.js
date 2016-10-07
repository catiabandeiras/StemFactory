// Module Pattern
// More information: http://toddmotto.com/mastering-the-module-pattern/

var Slem = (function ($) {
    // Prevents certain actions from being taken and throws exceptions
    "use strict";

    var _totalInvestment = 50000;
    var _incubatorValue = 15000;
    var _workerValue = 50;
    var _cabinetValue = 12000;
    var _incubatorCredits = 0;
    var _workerCredits = 0;
    var _cabinetCredits = 0;

    var _isSimS1NextButtonActive = false;
    var _isSimS2NextButtonActive = false;

    // Private functions
    var _init = function () {

        // Welcome messages fades
        $("#sim-welcome-msg").fadeIn(1000, function () {
            $("#sim-welcome-desc").fadeIn(1000, function () {
                $("#sim-welcome-start-btn-ctn").fadeIn(1000);
            });
        });

        // Start simulation button click event
        $("#sim-welcome-start-btn").on("click", function () {
            $("#sim-welcome-ctn").fadeOut(1000, function () {
                $("#sim-step1-ctn").fadeIn(1000);
            });
        });

        // Incubator add credit event
        $("#sim-s1-incubator-credit-add").on("click", function () {

            if (_totalInvestment - _incubatorValue > 0) {

                var creditsCtn = $("#sim-s1-incubator-credits");

                var credits = parseFloat(creditsCtn.text());

                creditsCtn.text(credits + 1);

                _totalInvestment = _totalInvestment - _incubatorValue;

                $("#sim-total").html(_totalInvestment + "&euro;");

                _incubatorCredits = _incubatorCredits + 1;
            }
        });

        // Incubator sub credit event
        $("#sim-s1-incubator-credit-sub").on("click", function () {

            if (_incubatorCredits > 0) {

                var creditsCtn = $("#sim-s1-incubator-credits");

                var credits = parseFloat(creditsCtn.text());

                creditsCtn.text(credits - 1);

                _totalInvestment = _totalInvestment + _incubatorValue;

                $("#sim-total").html(_totalInvestment + "&euro;");

                _incubatorCredits = _incubatorCredits - 1;
            }
        });

        // Worker add credit event
        $("#sim-s1-worker-credit-add").on("click", function () {

            if (_totalInvestment - _workerValue >= 0) {

                var creditsCtn = $("#sim-s1-worker-credits");

                var credits = parseFloat(creditsCtn.text());

                creditsCtn.text(credits + 1);

                _totalInvestment = _totalInvestment - _workerValue;

                $("#sim-total").html(_totalInvestment + "&euro;");

                _workerCredits = _workerCredits + 1;
            }
        });

        // Worker sub credit event
        $("#sim-s1-worker-credit-sub").on("click", function () {

            if (_workerCredits > 0) {

                var creditsCtn = $("#sim-s1-worker-credits");

                var credits = parseFloat(creditsCtn.text());

                creditsCtn.text(credits - 1);

                _totalInvestment = _totalInvestment + _workerValue;

                $("#sim-total").html(_totalInvestment + "&euro;");

                _workerCredits = _workerCredits - 1;
            }
        });

        // Cabinet add credit event
        $("#sim-s1-cabinet-credit-add").on("click", function () {

            if (_totalInvestment - _cabinetValue >= 0) {

                var creditsCtn = $("#sim-s1-cabinet-credits");

                var credits = parseFloat(creditsCtn.text());

                creditsCtn.text(credits + 1);

                _totalInvestment = _totalInvestment - _cabinetValue;

                $("#sim-total").html(_totalInvestment + "&euro;");

                _cabinetCredits = _cabinetCredits + 1;
            }
        });

        // Cabinet sub credit event
        $("#sim-s1-cabinet-credit-sub").on("click", function () {

            if (_cabinetCredits > 0) {

                var creditsCtn = $("#sim-s1-cabinet-credits");

                var credits = parseFloat(creditsCtn.text());

                creditsCtn.text(credits - 1);

                _totalInvestment = _totalInvestment + _cabinetValue;

                $("#sim-total").html(_totalInvestment + "&euro;");

                _cabinetCredits = _cabinetCredits - 1;
            }
        });

        // Next Step button color update event
        $(".check-next-step").on("click", function () {

            if(_incubatorCredits > 0 && _workerCredits > 0 && _cabinetCredits > 0)
            {
                $("#sim-s1-next-btn").removeClass("btn-default").addClass("btn-success");

                _isSimS1NextButtonActive = true;
            }
            else if(_isSimS1NextButtonActive) {

                $("#sim-s1-next-btn").removeClass("btn-success").addClass("btn-default");

                _isSimS1NextButtonActive = false;
            }
        });

        // Next button click event from Step 1 to Step 2
        $("#sim-s1-next-btn").on("click", function () {

            if (_isSimS1NextButtonActive) {

                $("#sim-step1-ctn").fadeOut(1000, function () {

                    $("#sim-step2-ctn").fadeIn(1000);

                    $("#sim-s2-total").html(_totalInvestment + "&euro;");
                });
            }
        });

        // Cocktail A select event
        $("#sim-s2-cocktailA-add").on("click", function () {

            $("#sim-s2-cocktailA-painel").removeClass("panel-primary").addClass("panel-success");
            $("#sim-s2-cocktailB-painel").removeClass("panel-success").addClass("panel-primary");
            $("#sim-s2-next-btn").removeClass("btn-default").addClass("btn-success");
            _isSimS2NextButtonActive = true;
        });

        // Cocktail A select event
        $("#sim-s2-cocktailB-add").on("click", function () {

            $("#sim-s2-cocktailB-painel").removeClass("panel-primary").addClass("panel-success");
            $("#sim-s2-cocktailA-painel").removeClass("panel-success").addClass("panel-primary");
            $("#sim-s2-next-btn").removeClass("btn-default").addClass("btn-success");
            _isSimS2NextButtonActive = true;
        });

        // Next button click event from Step 2 to Step 3
        $("#sim-s2-next-btn").on("click", function () {

            if (_isSimS2NextButtonActive) {

                $("#sim-step2-ctn").fadeOut(1000, function () {

                    $("#sim-step3-ctn").fadeIn(1000);
                });
            }
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