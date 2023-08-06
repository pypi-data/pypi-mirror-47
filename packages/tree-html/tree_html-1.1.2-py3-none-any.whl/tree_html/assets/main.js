(function() {
  // Multi-Level Accordion Menu - by CodyHouse.co
  var accordionsMenu = document.getElementsByClassName('cd-accordion--animated');

	if( accordionsMenu.length > 0 && window.requestAnimationFrame) {
		for(var i = 0; i < accordionsMenu.length; i++) {(function(i){
			accordionsMenu[i].addEventListener('change', function(event){
				animateAccordion(event.target);
			});
		})(i);}

		function animateAccordion(input) {
			var bool = input.checked,
				dropdown =  input.parentNode.getElementsByClassName('cd-accordion__sub')[0];
			
			Util.addClass(dropdown, 'cd-accordion__sub--is-visible'); // make sure subnav is visible while animating height

			var initHeight = !bool ? dropdown.offsetHeight: 0,
				finalHeight = !bool ? 0 : dropdown.offsetHeight;

			Util.setHeight(initHeight, finalHeight, dropdown, 200, function(){
				Util.removeClass(dropdown, 'cd-accordion__sub--is-visible');
				dropdown.removeAttribute('style');
			});
		}
	}
}());

// Codyhouse License below:
// The MIT License (MIT)
//
// Copyright (c) 2014-2019 Amber Creative Lab, Ltd.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.