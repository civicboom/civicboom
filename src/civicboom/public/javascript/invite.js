function inviteClick(eO) {
	var button        = $(eO);
	var form 		  = button.parents('form');
	var exclude_members = form.find('.exclude-members').val().split(',');
	var button_name   = button.attr('name');
	if (button_name  == 'Invite') return true;
	var button_action = button_name.split('-',1)[0];
	var button_key    = button_name.substring(button_name.search('-')+1)
	
	offset = getValue(button,'invitee-offset');
	limit  = getValue(button,'search-limit');
	ul     = button.parents('form').find('.invitee_ul');
	
	switch (button_action) {
		case 'add':
			if (exclude_members.contains(button_key)) {
				// Already exists in invitee list!
				return false;
			}
			var invitee_ul = button.parents('form').find('.invitee_ul');
			var li = button.parents('li').detach();
			invitee_ul.prepend(li);
			invitee_ul.children('li.none').remove();
			exclude_members.push(button_key);
			form.find('.exclude-members').val(exclude_members.join(','));
			li.append('<input type="hidden" class="username" name="inv-' + (exclude_members.length - 1) + '" value="' + button_key + '" />');
			button.html(button.val('Remove').attr('name', 'rem-' + (exclude_members.length - 1)).html().replace('i_plus_blue','i_delete').replace('Add','Remove'));
			refreshSearch(button);
		break;
		case 'rem':
			var li = button.parents('li');
			var ul = button.parents('ul');
			var username = li.find('input.username').val();
			// remove username from exclude list
			exclude_members = exclude_members.remove(username);
			form.find('.exclude-members').val(exclude_members.join(','));
			refreshSearch(button);
			li.remove();
			if (ul.find('li').length == 0)
				ul.append('<li class="none">Select people to invite from the right</li>');
		break;
		case 'search':
			refreshSearch(button, [{ 'name':button_name }]);
			return false;
		case 'invitee':
			switch (button_key) {
				case 'next':
					offset = offset + limit;
				break;
				case 'prev':
					if (offset - limit <= 0) {
						offset = 0;
					} else {
						offset = offset - limit;
					}
				break;
			}
		break;
	}
	setValue(button,'invitee-offset', offset);
	setValue(button,'search-limit', limit);
	listPaginate(ul, offset, limit, form.find('input[name="invitee-prev"]'), form.find('input[name="invitee-next"]'));
	
	return false;
}
function refreshSearch(element, extra_fields) {
	var form = element.parents('form');
	var exclude_members = form.find('.exclude-members').val().split(',');
	var ul = form.find('.invite-list');
	var formArray = formArrayNoPlaceholders(form);
	if (typeof extra_fields != 'undefined')
		formArray = formArray.concat(extra_fields);
	formArray.push({'name': 'exclude-members', 'value': exclude_members});
	$.post('/invite/search.frag', formArray, function (data) {
		ul.html(data);
		ul.children('.search-offset').val()
	});
}
function postInviteFrag(element, extra_fields) {
	var form = element.parents('form');
	var frag = form.parents('.frag_container');
	var formArray = formArrayNoPlaceholders(form);
	if (typeof extra_fields != 'undefined')
		formArray = formArray.concat(extra_fields);
	if (typeof element.attr('name') != 'undefined')
		formArray.push({'name': element.attr('name'), 'value': element.val()});
	$.post("/invite/index.frag", formArray, function (data) {
		frag.html(data);
	});
	return false;
}
function formArrayNoPlaceholders(form) {
	var formArray = form.serializeArray();
	var placeheld = form.find('input[placeholder]');
	if (placeheld.length > 0)
		for (var i = 0; i < placeheld.length; i++) {
			var elemjq = $(placeheld[i]);
			if (typeof elemjq.attr('placeholder') != 'undefined') {
				for (var j = 0; j < formArray.length; j++) {
					if (formArray[j].name == elemjq.attr('name')) {
						if (formArray[j].value == elemjq.attr('placeholder'))
							formArray[j].value = '';
						break;
					}
				}
			}
		}
	return formArray;
}
function getValue(element, cls) {
	return element.parents('form').find('.'+cls).val() * 1;
}
function setValue(element, cls, val) {
	return element.parents('form').find('.'+cls).val(val);
}
function listPaginate(ul, offset, limit, prev, next) {
	var visible = ul.children('li:eq('+offset+'),li:gt('+offset+')').filter('li:lt('+limit+')').css('display','inline-block');
	var hidden  = ul.children('li').not(visible).css('display','none');
	
	if (typeof prev != 'undefined')
		if (offset > 0) {
			prev.removeClass('disabled').attr('disabled','');
		} else {
			prev.addClass('disabled').attr('disabled','disabled');
		}
	if (typeof next != 'undefined')
		if ((offset + limit) < ul.children('li').length) {
			next.removeClass('disabled').attr('disabled','');
		} else {
			next.addClass('disabled').attr('disabled','disabled');
		}
	
}