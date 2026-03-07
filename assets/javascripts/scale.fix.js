fixScale = function(doc) {
	// Guard against running twice (pages may call fixScale and this file also auto-runs it).
	if (doc.__fixScaleInitialized) return;
	doc.__fixScaleInitialized = true;

	var qsa = 'querySelectorAll';

	// External links open in a new tab so visitors keep this homepage open.
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

};

if (typeof document !== 'undefined') fixScale(document);
