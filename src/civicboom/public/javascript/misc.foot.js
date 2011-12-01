// janrain_app_id is set at the top of the footer scripts, then
// misc.foot.js is loaded in the middle of the footer
// RPXNOW is not loaded in offline (demo) mode, initialising it breaks all javascript
if (typeof RPXNOW !== 'undefined') {
  RPXNOW.init({appId: janrain_app_id, xdReceiver: '/rpx_xdcomm.html'});
}
if (typeof addthis == 'undefined' || typeof (addthis || {}).toolbox == 'undefined') {
  addthis = {toolbox:function(){}};
}

// Run any boom.init_foot functions
for (var i in boom.init_foot) {
  boom.init_foot[i]();
}

// Variables: share_display, share_usergen_default, action_share_description, action_page_title, action_page_description, action_links, properties, images, audio, video
function janrain_popup_share(url, options, variables) {
  // RPXNOW is not loaded in offline (demo) mode
  if (typeof RPXNOW === 'undefined')
    return;
	RPXNOW.loadAndRun(['Social'], function () {
		if (typeof options != 'object') options = {};
		var activity = new RPXNOW.Social.Activity(variables.share_display,
												  variables.action_share_description,
												  url
												  );
		
		activity.setTitle               (variables.action_page_title);
		activity.setDescription         (variables.action_page_description);
		activity.setUserGeneratedContent(variables.share_usergen_default);
		
		if (typeof variables.action_links == 'object') {
			for (i=0; i<variables.action_links.length; i++) {
				activity.addActionLink(variables.action_links[i].text, variables.action_links[i].href);
			}
		}
		
		/*
		if (typeof variables.properties == 'object') {
			for (i=0; i<variables.properties.length; i++) {
				activity.addTextProperty(variables.properties[i].text, variables.properties[i].value);
			}
		}
		*/
		
		if (typeof variables.media == 'object') {
			var rpx_images;
			for (i=0; i<variables.media.length; i++) {
				var media = variables.media[i];
				if (media.type=='image') {
					if (typeof rpx_images == 'undefined')
						rpx_images = new RPXNOW.Social.ImageMediaCollection();
					rpx_images.addImage(media.src, media.href);
				} else if (media.type=='audio') {
					activity.setMediaItem(new RPXNOW.Social.Mp3MediaItem(media.src));
				} else if (media.type=='video') {
					var rpx_video = new RPXNOW.Social.VideoMediaItem(
						media.original_url,
						media.thumbnail_url
					);
					rpx_video.setVideoTitle(variables.video[i].caption);
					activity.setMediaItem(rpx_video);
				}
			}
			if (typeof rpx_images != 'undefined')
				activity.setMediaItem(rpx_images); 
		}
		
		var finished = function(results) {
		  // Process results of publishing.
		}
		
		options.finishCallback = finished;
		options.urlShortening = true;
		
		RPXNOW.Social.publishActivity(activity, options);
	});
}
