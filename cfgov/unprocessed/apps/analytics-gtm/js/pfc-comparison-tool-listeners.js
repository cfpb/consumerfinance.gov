// Paying for College custom analytics file

var PFCAnalytics = (function() {
    var $ = window.jQuery;

    //-- Delay calculations after keyup --//
    var delay = (function(){
            var t = 0;
            return function(callback, delay) {
                clearTimeout(t);
                t = setTimeout(callback, delay);
            };
    })(); // end delay()

    //-- findEmptyColumn() - finds the first empty column, returns column number [1-3] --//
    function findEmptyColumn() {
        var column = false;
        for (var x = 1; x <= 3; x++) {
            var school_id = $("#institution-row [data-column='" + x + "']").attr("data-schoolid");
            if ( school_id === "" ) {
                column = x;
                break;
            }
        }
        return column;
    } // end findEmptyColumn()

    var global = {
        'schoolsAdded': 0, 'emptyColumn': 1
    }
    var rateChangeClicks = [];
    var schoolsZeroed = ['example'];

    // Fire an event when a school is removed.
    $('.remove-confirm .remove-yes').click( function() {
        var columnNumber = $(this).parents('[data-column]').attr('data-column');
        var schoolID = $('#institution-row [data-column="' + columnNumber + '"]').attr('data-schoolid');
        dataLayer.push({
            "event": "School Interactions",
            "action": "School Cost Comparison",
            "label": "School Removed"
        });
        // Important to add a School tracking - reset the global.emptyColumn var
        global.emptyColumn = findEmptyColumn();
    });

    // Fire an event when Left to Pay = $0 and Costs > $0
    $('#comparison-tables').on('keyup', 'input.school-data', function (ev) {
        var columnNumber = $(this).parents('[data-column]').attr('data-column');
        delay(function(){
            var totalCosts = $('.breakdown [data-column="' + columnNumber + '"] .costs-value').html();
            var leftToPay = $('.breakdown [data-column="' + columnNumber + '"] [data-nickname="gap"]').html();
            var schoolID = $('#institution-row [data-column="' + columnNumber + '"]').attr('data-schoolid');
            if (leftToPay === "$0" && totalCosts !== "$0") {
                dataLayer.push({
                    "event": "School Interactions",
                    "action": "Reached Zero Left to Pay",
                    "label": schoolID
                });
            }
        }, 1000);
    });

    // Fire an event when a tooltip is clicked
    $(".tooltip-info").click( function(event) {
        var tooltip = $(this).attr("data-tipname");
        dataLayer.push({
            "event": "School Interactions",
            "action": "Tooltip Clicked",
            "label": tooltip
        });
    });

    // Fire an event when GI Bill panel opens
    $(".gibill-calculator, input[data-nickname='gibill']").click(function() {
        var columnNumber = $(this).parents('[data-column]').attr('data-column');
        var schoolID = $("#institution-row [data-column='" + columnNumber + "']").attr("data-schoolid");
        delay(function() {
            var GIPanel = $('[data-column="' + columnNumber + '"] .gibill-panel');
            if (GIPanel.is(':visible')) {
                dataLayer.push({
                    "event": "School Interactions",
                    "action": "GI Bill Calculator Opened",
                    "label": schoolID
                });
            }
        }, 500);
    });

    // Fire various events for rate-change clicks
    $('.rate-change').click(function() {
        var buttonID = $(this).attr('data-buttonid');
        if (jQuery.inArray(buttonID, rateChangeClicks) === -1) {
            rateChangeClicks.push(buttonID);
            dataLayer.push({
                "event": "School Interactions",
                "action": "Percent Arrow Clicked",
                "label": buttonID
            });
        }

    })

    // Fire an event when clicking "Calculate" button
    $(".gibill-panel .military-calculate").click( function() {
        var columnNumber = $(this).closest("[data-column]").attr("data-column");
        var schoolID = $("#institution-row [data-column='" + columnNumber + "']").attr("data-schoolid");
        var serving = $('[data-column="1"] .military-status-select :selected').html();
        var tier = $("[data-column='1'] .military-tier-select").find(":selected").html();
        var residency = $("[data-column='1'] .military-residency-panel :radio:checked").val();
        var control = $('.header-cell[data-column="' + columnNumber + '"]').attr('data-control');

        dataLayer.push({
            "event": "School Interactions",
            "action": "GI Bill Calculator Submit",
            "label": schoolID
        });
        dataLayer.push({
            "event": "School Interactions",
            "action": "Military Status",
            "label": serving
        });
        dataLayer.push({
            "event": "School Interactions",
            "action": "Cumulative service",
            "label": tier
        });
        if (control == "Public") {
            dataLayer.push({
                "event": "School Interactions",
                "action": "GI Residency",
                "label": residency
            });
        }
    });

    // Fire an event when Send Email is clicked
    $("#send-email").click( function(){
        dataLayer.push({
            "event": "School Interactions",
            "action": "Save and Share",
            "label": "Send email"
        });
    });

    // Fire an event when save draw is opened
    $("#save-and-share").click( function( event, nateeve ) {
        if ( nateeve == undefined) {
            dataLayer.push({
                "event": "School Interactions",
                "action": "Save and Share",
                "label": "toggle button"
            });
        }
    });

    // Fire an event when save current is clicked
    $("#save-current").click( function() {
        dataLayer.push({
            "event": "School Interactions",
            "action": "Save and Share",
            "label": "Save current worksheet"
        });
    });

    $("#unique").click( function() {
        dataLayer.push({
            "event": "School Interactions",
            "action": "Save and Share",
            "label": "Copy URL"
        });
    });

    $("#save-drawer .save-share-facebook").click( function() {
        dataLayer.push({
            "event": "School Interactions",
            "action": "Save and Share",
            "label": "Facebook_saveshare"
        });
    });

    $("#save-drawer .save-share-twitter").click( function() {
        dataLayer.push({
            "event": "School Interactions",
            "action": "Save and Share",
            "label": "Twitter_saveshare"
        });
    });

    // Fire an event when Get Started is clicked
    $('#get-started-button').click(function() {
        dataLayer.push({
            "event": "School Interactions",
            "action": "School Cost Comparison",
            "label": "Get Started Button"
        });
    });

    // Fire an event when Add a School is cancelled
    $('#introduction .add-cancel').click( function() {
        dataLayer.push({
            "event": "School Interactions",
            "action": "School Cost Comparison",
            "label": "Cancel Button"
        });
    });

    // Fire an event when Continue is clicked
    $('#introduction .continue').click( function() {
        dataLayer.push({
            "event": "School Interactions",
            "action": "School Cost Comparison",
            "label": "Continue Button"
        });
        console.log('#introduction .continue clicked');
    });

    // Fire an event when Add another school is clicked
    $('#introduction .add-another-school').click( function() {
        dataLayer.push({
            "event": "School Interactions",
            "action": "School Cost Comparison",
            "label": "Add another school Button"
        });
    });

    // Fire an event when adding a school.
    function newSchoolEvent() {
        var schoolID = $("#school-name-search").attr("data-schoolid");
        var program = $('#step-two input:radio[name="program"]:checked').val();
        var kbyoss = $("#school-name-search").attr("data-kbyoss");
        var prgmlength = String($('#step-two select[name="prgmlength"]').val());
        var housing = $('input[name="step-three-housing"]:checked').val();
        var control = $("#school-name-search").attr("data-control");
        var residency = $('input[name="step-three-residency"]:checked').val();
        var offer = "No";

        global.schoolsAdded++;
        var schoolCount = String(global.schoolsAdded);
        if ( $("#finaidoffer").is(":checked")) {
            offer = "Yes";
        }
        dataLayer.push({
            "event": "School Interactions",
            "action": "Total Schools Added",
            "label": schoolCount
        });
        dataLayer.push({
            "event": "School Interactions",
            "action": "School Added",
            "label": schoolID
        });
        dataLayer.push({
            "event": "School Interactions",
            "action": "Program Type",
            "label": program
        });
        dataLayer.push({
            "event": "School Interactions",
            "action": "Program Length",
            "label": prgmlength
        });


        if (offer === "Yes") {
            dataLayer.push({
                "event": "School Interactions",
                "action": "Financial Aid Clicked"
            });
            if ( $('#xml-text').val() === "" &&  kbyoss == "Yes") {
                dataLayer.push({
                    "event": "School Interactions",
                    "action": "School Added - XML",
                    "label": "Blank"
                });
            }
            else if ( $('#xml-text').val() !== "" && kbyoss == "Yes") {
                dataLayer.push({
                    "event": "School Interactions",
                    "action": "School Added - XML",
                    "label": "XML text"
                });
            }
        }

        else {
            dataLayer.push({
                "event": "School Interactions",
                "action": "Housing",
                "label": housing
            });
            if (control == "Public") {
                dataLayer.push({
                    "event": "School Interactions",
                    "action": "Residency",
                    "label": residency
                });
            }
        }
    }

    // Check for a new school added when .continue and .add-another-school are clicked
    $('#introduction .continue, #introduction .add-another-school').click( function() {
        delay(function() {
            var newEmpty = findEmptyColumn();
            if (newEmpty != global.emptyColumn) {
                newSchoolEvent();
                global.emptyColumn = newEmpty;
            }
        }, 500);

    });

    // Fire event when user clicks the arrows to open sections
    $('.arrw-collapse').click(function() {
        var arrwName = $(this).attr('data-arrwname');
        dataLayer.push({
            "event": "School Interactions",
            "action":"Drop Down",
            "label": arrwName
        });
    });


})(jQuery);
