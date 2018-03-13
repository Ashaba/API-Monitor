const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const { window } = new JSDOM(`...`);
global.$ = require('jquery')(window);
const assert = require('chai').assert;
const sinon = require('sinon');
const dashboard = require('../dashboard').main;

describe('Dashboard', function() {

    describe('addElement', function() {
        var container;

        it('Adds element e.g check', function() {
            container = $('<div>').attr('id', 'checks');
            var event = {
                data: {
                    container: container,
                    template: dashboard.checkTemplate
                }
            }
            dashboard.addElement(event);

            assert.equal(container.children().length, 1);
        });
    })

    describe('removeElement', function() {
        var container;

        it('Removes element e.g header', function() {
            container = $('<div>').attr('id', 'headers');
            var event = {
                data: {
                    container: container,
                    template: dashboard.requestHeaderTemplate
                }
            }
            dashboard.addElement(event);
            const header = container.children();
            removeButton = header.children('.removeHeader');
            event = {
                data: {
                    element: removeButton
                }
            }
            dashboard.removeParent(event);

            assert.equal(container.children().length, 0);
        });
        
    })

    describe('getFormData', function() {
        
        it('Gets data from form', function() {
            var check = $($.trim(dashboard.checkTemplate));
            var form = check.find('.form');

            var data = dashboard.getFormData(form);

            assert.isFalse($.isEmptyObject(data));

        });

    })

    describe('postData', function() {
        
        it('Does not post non array data', function() {
            assert.isFalse(dashboard.postData('some data'));
        });

        it('Does not post empty data', function() {
            assert.isFalse(dashboard.postData([]));
        });

        it('It posts array data', function() {
            data = ['test', 'data'];
            const callback = sinon.spy();
            const ajax = sinon.stub($, 'ajax');
            ajax.yieldsTo('success');

            dashboard.postData(data, callback);

            sinon.assert.calledOnce(callback);
            ajax.restore();
            
        });

    })

});
