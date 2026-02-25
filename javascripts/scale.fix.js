fixScale = function(doc) {
	if (doc.__fixScaleInitialized) return;
	doc.__fixScaleInitialized = true;

	var addEvent = 'addEventListener',
	    type = 'gesturestart',
	    qsa = 'querySelectorAll',
	    scales = [1, 1],
	    meta = qsa in doc ? doc[qsa]('meta[name=viewport]') : [];

	if (qsa in doc && doc.location) {
		var links = doc[qsa]('a[href]');
		for (var i = 0; i < links.length; i++) {
			var link = links[i];
			var href = link.getAttribute('href');
			if (!href || href.charAt(0) === '#' || href.indexOf('mailto:') === 0 || href.indexOf('tel:') === 0) continue;
			if (link.hostname && link.hostname !== doc.location.hostname) {
				link.setAttribute('target', '_blank');
				link.setAttribute('rel', 'noopener noreferrer');
			}
		}
	}

	function fix() {
		meta.content = 'width=device-width,minimum-scale=' + scales[0] + ',maximum-scale=' + scales[1];
		doc.removeEventListener(type, fix, true);
	}

	if ((meta = meta[meta.length - 1]) && addEvent in doc) {
		fix();
		scales = [.25, 1.6];
		doc[addEvent](type, fix, true);
	}

};

if (typeof document !== 'undefined') fixScale(document);
