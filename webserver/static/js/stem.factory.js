// Module Pattern
// More information: http://toddmotto.com/mastering-the-module-pattern/

var Slem = (function ($) {
    // Prevents certain actions from being taken and throws exceptions
    "use strict";


    var flat_clone_obj = function(obj) {
        if (obj === null || typeof obj !== 'object') return obj;

        var temp = obj.constructor(); // give temp the original obj's constructor
        for (var key in obj) temp[key] = obj[key]; // flat_clone_obj(...)

        return temp;
    }

    var _balance =      parseFloat($('#balance').val(), 10);

    var _assetPrices = {
        'incubator':    parseFloat($('#incubator-data') .data('price'), 10),
        'worker':       parseFloat($('#worker-data')    .data('price'), 10),
        'cabinet':      parseFloat($('#cabinet-data')   .data('price'), 10),
        'bioreactor':   parseFloat($('#bioreactor-data').data('price'), 10)
    };

    var _currentAssets = {
        'incubator':    parseInt($('#TOTAL_INCUBATORS')   .val()),
        'worker':       parseInt($('#TOTAL_WORKERS')      .val()),
        'cabinet':      parseInt($('#TOTAL_BSC')          .val()),
        'bioreactor':   parseInt($('#TOTAL_BIOREACTORS')  .val())
    };

    var _pastAssets = flat_clone_obj(_currentAssets);


    var _isSimS1NextButtonActive = false;
    var _isSimS2NextButtonActive = false;

    var animationTime = 600

    // Private functions
    var _init = function () {

        // Welcome messages fades
        $("#sim-welcome-msg").fadeIn(animationTime, function () {
            $("#sim-welcome-desc").fadeIn(animationTime, function () {
                $("#sim-instructions").fadeIn(animationTime, function () {
                    $("#sim-welcome-start-btn-ctn").fadeIn(animationTime);
                 });
            });
        });

        // Start simulation button click event
        $("#sim-welcome-start-btn").on("click", function () {
            $("#sim-welcome-ctn").fadeOut(animationTime, function () {
                $("#sim-step1-ctn").fadeIn(animationTime);
            });
        });

        for (var assetId in _currentAssets) {
            var uiAmount = $('#' + assetId + '-units');
            if (uiAmount) uiAmount.text(_currentAssets[assetId]);
        }

        var lookup_elem_by_data = function(elem, dataId)
        {
            while(elem) {
                var val = elem.data(dataId);
                if (val) return elem;
                elem = elem.parent();
            }
        }

        var fetch_asset_entities = function(touchedElem)
        {
            var dataElem = lookup_elem_by_data($(touchedElem), 'price');
            var price = dataElem.data('price');
            var elemId = dataElem.data('id');
            var formElem = $('#' + dataElem.data('field'));
            var uiElem = $('#' + elemId + '-units');
            return {
                id:         elemId,
                price:      price,
                uiElem:     uiElem,
                formElem:   formElem,
                min:        _pastAssets[elemId]
            };
        }

        var update_balance = function(transactionAmount){
            _balance = _balance + transactionAmount
            $(".sim-balance").html(_balance + "&euro;");
        }

        var update_asset_units = function(asset, units) {
            asset.uiElem.text(units);
            asset.formElem.val(units);
            _currentAssets[asset.id] = units
        }

        var add_asset = function() {
            var asset = fetch_asset_entities(this);
            if (_balance - asset.price > 0) {
                var units = parseInt(asset.formElem.val(), 10);
                units++;
                update_asset_units(asset, units);
                update_balance(- asset.price);
            }
            return false;
        }

        var sub_asset = function() {

            var asset = fetch_asset_entities(this);
            var units = parseInt(asset.formElem.val(), 10);

            if (units > _pastAssets[asset.id]) {
                units--;
                update_asset_units(asset, units);
                update_balance(+ asset.price);
            }
            return false;
        }

        var consumable_select = function()
        {
            $(".consumables-panel").removeClass("panel-success").addClass("panel-primary"); // reset

            var elem = lookup_elem_by_data($(this), 'growth');

            elem.removeClass("panel-primary").addClass("panel-success");
            $("#sim-s2-next-btn").removeClass("btn-default").addClass("btn-success");
            _isSimS2NextButtonActive = true;

            //copy params to form
            var growth = elem.data('growth'); // jquery auto decodes array??? very nice!
            if (growth.constructor === Array)
            {
                for (var g in growth)
                    $('#GR_P' + (parseInt(g, 10) + 1)).val(growth[g]); // g is a string - jquery thing?
            }
            return false;
        }

        var submit_simulation = function() { $('#simulation-form').submit(); }

        // add / sub asset event
        $(".units-sub").on("click", sub_asset);
        $(".units-add").on("click", add_asset);

        // Cocktail select event
        $(".consumable-select").on("click", consumable_select);


        // Next Step button color update event
        $(".check-next-step").on("click", function () {

            if(_currentAssets['incubator'] > 0 && _currentAssets['worker'] > 0 && _currentAssets['cabinet'] > 0)
            {
                $("#sim-s1-next-btn").removeClass("btn-default").addClass("btn-success");

                _isSimS1NextButtonActive = true;
            }
            else if(_isSimS1NextButtonActive) {

                $("#sim-s1-next-btn").removeClass("btn-success").addClass("btn-default");

                _isSimS1NextButtonActive = false;
            }
            return false;
        });

        // Next button click event from Step 1 to Step 2
        $("#sim-s1-next-btn").on("click", function () {

            if (_isSimS1NextButtonActive) {

                $("#sim-step1-ctn").fadeOut(animationTime, function () {

                    $("#sim-step2-ctn").fadeIn(animationTime);

//                    $("#sim-s2-total").html(_balance + "&euro;");
                });
            }
            return false;
        });

        // Next button click event from Step 2 to Step 3
        $("#sim-s2-next-btn").on("click", function () {

            if (_isSimS2NextButtonActive) {

                $("#sim-step2-ctn").fadeOut(animationTime, function () {

                    $("#sim-step3-ctn").fadeIn(animationTime);
                });
            }
            setTimeout(submit_simulation, 100);
            return false;
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
