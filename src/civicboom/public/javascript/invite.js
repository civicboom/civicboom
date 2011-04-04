function inviteClick(eO) {
	var button        = $(eO);
	var form 		  = button.parents('form');
	var exclude_members = form.find('.exclude-members').val().split(',');
	var button_name   = button.attr('name');
	if (button_name  == 'Invite') return true;
	var button_action = button_name.split('-',1)[0];
	var button_key    = button_name.split('-',2)[1];
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
			button.html(button.val('Remove').attr('name', 'rem-' + (exclude_members.length - 1)).html().replace('i_plus','i_delete').replace('Add','Remove'));
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
			break;
		case 'invitee':
			offset = getValue(button,'invitee-offset');
			limit  = getValue(button,'search-limit');
			ul     = button.parents('form').find('.invitee_ul');
			switch (button_key) {
				case 'next':
					if (offset + limit <= ul.find('li').count) {
						offset = offset + limit;
						ul.parents('form').find('.invitee-prev').attr('disabled','');
					} else {
						ul.parents('form').find('.invitee-prev').attr('disabled','disabled');
					}
				break;
				case 'prev':
					if (offset - limit <= 0) {
						offset = 0;
						ul.parents('form').find('.invitee-prev').attr('disabled','disabled');
						
					} else {
						offset = offset - limit;
					}
					ul.parents('form').find('.invitee-next').attr('disabled','');
				break;
			}
			
			listPaginate(ul, offset, limit);
			break;
	}
	return false;
}
function refreshSearch(element, extra_fields) {
	var form = element.parents('form');
	var exclude_members = form.find('.exclude-members').val().split(',');
	var ul = form.find('.invite-list');
	var formArray = form.serializeArray();
	if (typeof extra_fields != 'undefined')
		formArray = formArray.concat(extra_fields)
	formArray.push({'name': 'exclude-members', 'value': exclude_members});
	$.post('/invite/search.frag', formArray, function (data) {
		ul.html(data);
		ul.children('.search-offset').val()
	});
}
function getValue(element, class) {
	return element.parents('form').find('.'+class).val() * 1;
}
function listPaginate(ul, offset, limit) {
	var visible = ul.children('li:eq('+offset+'),li:gt('+offset+')').filter('li:lt('+limit+')').css('display','inline-block');
	var hidden  = ul.children('li').not(visible).css('display','none');
}