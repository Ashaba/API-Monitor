var resultTemplate = `
    <div class="result">
        <div class="result__Header">
            <div class="result_Arrow"><span class="fa fa-caret-right"></span></div>
            <span class="result__Url"></span>
            <div class="result__Response">
                <span class="result__StatusCode">
                    <span class="fa fa-circle"></span>
                    <span class="result__StatusCodeValue"></span>
                </span>
                <span class="result__ResponseTime">
                    <span class="fa fa-clock"></span>
                    <span class="result__ResponseTimeValue"></span>
                </span>    
                <button class="result__EditCheck"><span class="fa fa-pencil-alt"></span> Edit</button>
            </div>
        </div>
        <span class="result__Method">GET/</span>
        <p class="result__AssertionsHeading">ASSERTIONS</p>
        <div class="result__Assertions"></div>
        <div class="result_More"></div>
    </div>
`,
assertionTemplate = `
    <p class="result__Assertion">
        <span class="result__AssertionIcon fa"></span>
        <span class="result__AssertionText"> Status — '200' was a number equal to 200</span>
    </p>
`,
resultSummaryTemplate = `
<a class="nav-link resultSummary" data-toggle="tab" href="#results" role="tab">
    <div class="resultSummary__StatusContainer">
        <div class="resultSummary__Status">
            <i class="fa resultSummary__StatusIcon"></i>
            <span class="resultSummary__StatusText">Failed</span>
        </div>
        <p class="resultSummary_Failures">2 failures</p>
    </div>
    <div class="resultSummary_briefDetails">
        <p class="resultSummary__Date">Mar 15 6:17pm</p>
        <p class="resultSummary__RunFrom">via Dashboard</p>
    </div>
</a>
`;

$.each(context.results, function(index, resultsSet) {
    createResultSummary(index, resultsSet.summary);
    $.each(resultsSet.results, function(index2, resultData) {
        createResult(index, resultData);
    });
});

function createResult(containerIndex, resultData) {
    var result = $($.trim(resultTemplate));
    result.attr('id', resultData.id);
    result.find('.result__Url').html(resultData.url);
    result.find('.result__StatusCodeValue').html(resultData.statusCode);
    result.find('.result__ResponseTimeValue').html(resultData.responseTime);
    result.find('.result__Method').html(resultData.method);
    result.find('.result_Arrow').on('click', function() {
        var moreResults = result.find('.result_More');
        if (moreResults.is(':visible')) {
            moreResults.hide();
        } else {
            moreResults.show();
        }
    });

    $.each(resultData.assertions, function(index, assertion) {
        createAssertion(result, assertion);
    });
    
    result.appendTo($(`#results${containerIndex}`));
}

function createAssertion(result, assertionData) {
    var assertion = $($.trim(assertionTemplate)),
        falsy = '';
    if(assertionData.status == 'success') {
        assertion.find('.result__AssertionIcon').addClass('fa-check');
    } else {
        assertion.find('.result__AssertionIcon').addClass('fa-times');
        falsy = 'not';
    }
    assertion.find('.result__AssertionText').html(`${assertionData.type} - '${assertionData.received}' was ${falsy} ${assertionData.comparison} ${assertionData.expected}`);
    
    assertion.appendTo(result.find('.result__Assertions'));
}

function createResultSummary(index, resultSummaryData) {
    var resultSummary = $($.trim(resultSummaryTemplate));
    resultSummary.attr('href',`#results${index}`);
    if(resultSummaryData.status == 'success') {
        resultSummary.find('.resultSummary__StatusIcon').addClass('fa-check').css('color', 'green');
    } else {
        resultSummary.find('.resultSummary__StatusIcon').addClass('fa-times').css('color', 'red');
    }
    resultSummary.find('.resultSummary__StatusText').html(resultSummaryData.status);
    resultSummary.find('.resultSummary_Failures').html(`${resultSummaryData.failures} failures`);
    resultSummary.find('.resultSummary__Date').html(resultSummaryData.date);
    resultSummary.find('.resultSummary__RunFrom').html(`via ${resultSummaryData.runFrom}`);
    resultSummary.appendTo($('.checkList .navLinks'));

    var fullResultsPane = $(`<div id="results${index}" class="tab-pane"></div>`);
    fullResultsPane.appendTo($('.resultsContainer'));
}


