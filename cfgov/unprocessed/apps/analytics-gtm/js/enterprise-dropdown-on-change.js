//no changes here
function addListener(element, type, callback) {
 if (element.addEventListener) element.addEventListener(type, callback);
 else if (element.attachEvent) element.attachEvent('on' + type, callback);
}

var mySelects = document.getElementsByTagName('span');
selectIndex=mySelects.length;
while(--selectIndex >= 0){
	addListener(mySelects[selectIndex],'change', function(){
		customEvent = {
			"event": "gtm.change",
			"gtm.element": this,
			"gtm.elementClasses": this.className,
			"gtm.elementId": this.id,
			"gtm.elementTarget": this.target
		};
		dataLayer.push(customEvent);
	});
};
