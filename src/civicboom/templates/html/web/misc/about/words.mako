Here are some words that are never used on their own in templates, but
might be dynamically generated on their own -- thus no translation is
automatically created but one is needed:

${_("_user")}
${_("_User")}
${_('_users')}
${_('_Users')}
${_('_group')}
${_('_Group')}
${_('_groups')}
${_('_Groups')}

${_("_free")}
${_("_Free")}
${_("_plus")}
${_("_Plus")}

${_("_article")}
${_("_Article")}
${_("_assignment")}
${_("_Assignment")}
${_("_request")}
${_("_Request")}
${_("_draft")}
${_("_Draft")}

${_("Offensive")}
${_("Spam")}
${_("Copyright")}

${_("Role")}
${_("Members")}

${_("admin")}
${_("Admin")}
${_("editor")}
${_("Editor")}
${_("contributor")}
${_("Contributor")}
${_("observer")}
${_("Observer")}

<%

share_data = {
        'user' : {
           'new': {
               'type': {
                    'assignment': _("I just posted a request for _content: %(title)s on _site_name. Respond now!"),
                    'response'  : _("I just responded to a request for _content by %(parent_owner)s on _site_name. Get involved & add your story too!"),
                    'group'     : _("I just created the %(name)s Hub on _site_name. Follow it now and get involved!"),
                    'user'      : _("I just signed up to _site_name to get my _articles published - you can too!"),
                    'article'   : _("I just created the content %(title)s on _site_name, check it out here!"),
                },
                'tag': {
                    'assignment': _("Share _assignment with your friends and followers:"),
                    'response'  : _("Share your _content with your friends and followers:"),
                    'group'     : _("Share _group with your friends and followers:"),
                    'user'      : _("Share your news _content with your friends and followers:"),
                    'article'   : _("Share _article with your friends and followers:"),
                },
                'desc': {
                    'assignment': _('New _assignment on _site_name'),
                    'response'  : _('New _article on _site_name'),
                    'group'     : _('New _group on _site_name'),
                    'user'      : _("I'm on _site_name"),
                    'article'   : _('New _article on _site_name'),
                },
            },
            'existing': {
               'type': {
                    'assignment': _("Check out my request for _content: %(title)s on _site_name. Share your _content now!"),
                    'response'  : _("Check out my _content - %(owner)s on _site_name. Get involved & add your _content!"),
                    'group'     : _("Check out my %(name)s Hub on _site_name. Follow it now and get involved!"),
                    'user'      : _("Check out my profile on _site_name. You can sign up too and get your _articles published!"),
                    'article'   : _("Check out my content %(title)s on _site_name!"),
                },
                'tag': {
                    'assignment': _("Share _assignment with your friends and followers:"),
                    'response'  : _("Share this _content response with your friends and followers:"),
                    'group'     : _("Share _group with your friends and followers:"),
                    'user'      : _("Share your profile with your friends and followers:"),
                    'article'   : _("Share _article with your friends and followers:"),
                },
                'desc': {
                    'assignment': _('My _assignment on _site_name'),
                    'response'  : _('My _article on _site_name'),
                    'group'     : _('My _group on _site_name'),
                    'user'      : _("I'm on _site_name"),
                    'article'   : _('My _article on _site_name'),
                },
            },
            'other': {
               'type': {
                    'assignment': _("Check out %(title)s on _site_name and share your story now!"),
                    'response'  : _("Check out this response to a request for a story by %(owner)s on _site_name. Get involved & add your story!"),
                    'group'     : _("Check out %(name)s Hub on _site_name. Follow it now and get involved!"),
                    'user'      : _("Check out %(name) on _site_name. They're getting their news published - and you can too!"),
                    'article'   : _("Check out %(title)s on _site_name!"),
                },
                'tag': {
                    'assignment': _("Share this _assignment with your friends and followers:"),
                    'response'  : _("Share this response with your friends and followers:"),
                    'group'     : _("Share this _group with your friends and followers:"),
                    'user'      : _("Share this news with your friends and followers:"),
                    'article'   : _("Share this _article with your friends and followers:"),
                },
                'desc': {
                    'assignment': _('_Assignment on _site_name'),
                    'response'  : _('_Article on _site_name'),
                    'group'     : _('_Group on _site_name'),
                    'user'      : _("Profile on _site_name"),
                    'article'   : _('_Article on _site_name'),
                },
            },
        },
        'group' : {
           'new': {
               'type': {
                    'assignment': _("We want your _content! Check out %(title)s on _site_name. Respond now for your chance to get published!"),
                    'response'  : _("We just shared our _content in response to %(owner)s on _site_name. Get involved & add your story!"),
                    'group'     : _("We just created the %(name)s Hub on _site_name. Follow it now to share your _articles!"),
                    'user'      : _("We just signed up to _site_name to get _articles from source - and you can too!"),
                    'article'   : _("We just created the content %(title)s on _site_name, check it out here!"),
                },
                'tag': {
                    'assignment': _("Share your _assignment with your friends and followers:"),
                    'response'  : _("Share your response with your friends and followers:"),
                    'group'     : _("Share your _group with your friends and followers:"),
                    'user'      : _("Share your news with your friends and followers:"),
                    'article'   : _("Share your _article with your friends and followers:"),
                },
                'desc': {
                    'assignment': _('New _assignment on _site_name'),
                    'response'  : _('New _article on _site_name'),
                    'group'     : _('New _group on _site_name'),
                    'user'      : _("We're on _site_name"),
                    'article'   : _('New _article on _site_name'),
                },
            },
            'existing': {
               'type': {
                    'assignment': _("Check out our request %(title)s on _site_name and share your _content!"),
                    'response'  : _("Check out our response to a request by %(owner)s on _site_name. Get involved & add your _content!"),
                    'group'     : _("Check out our %(name)s Hub on _site_name. Follow it now to share your _articles!"),
                    'user'      : _("Check out our profile on _site_name, join to get your news published!"),
                    'article'   : _("Check out our content %(title)s on _site_name!"),
                },
                'tag': {
                    'assignment': _("Share your _assignment with your friends and followers:"),
                    'response'  : _("Share your response with your friends and followers:"),
                    'group'     : _("Share your _group with your friends and followers:"),
                    'user'      : _("Share your profile with your friends and followers:"),
                    'article'   : _("Share your _article with your friends and followers:"),
                },
                'desc': {
                    'assignment': _('Our _assignment on _site_name'),
                    'response'  : _('Our _article on _site_name'),
                    'group'     : _('Our _group on _site_name'),
                    'user'      : _("We're on _site_name"),
                    'article'   : _('Our _article on _site_name'),
                },
            },
            'other': {
               'type': {
                    'assignment': _("Check out this _content request %(title)s on _site_name. Take a look and respond now!"),
                    'response'  : _("Check out this response to a request by %(owner)s on _site_name. Get involved & add your _content!"),
                    'group'     : _("Check out %(name)s Hub on _site_name. Get involved and follow it now!"),
                    'user'      : _("Check out %(name) on _site_name. You too can sign up and get your news published!"),
                    'article'   : _("Check out %(title)s on _site_name!"),
                },
                'tag': {
                    'assignment': _("Share this _assignment with your friends and followers:"),
                    'response'  : _("Share this response with your friends and followers:"),
                    'group'     : _("Share this _group with your friends and followers:"),
                    'user'      : _("Share this news with your friends and followers:"),
                    'article'   : _("Share this _article with your friends and followers:"),
                },
                'desc': {
                    'assignment': _('_Assignment on _site_name'),
                    'response'  : _('_Article on _site_name'),
                    'group'     : _('_Group on _site_name'),
                    'user'      : _("Profile on _site_name"),
                    'article'   : _('_Article on _site_name'),
                },
            },
        }
    }
%>



## From frag/contents/edit.mako:
<%
#        if selected_type == "assignment":
    confirm_title = _("Once you post this request, it will appear:")
    confirm_message = _("<ol>" +\
                "<li>" + "On your _Widget for your community to respond to" +"</li>" +\
                "<li>" + "In all your _site_name followers' notification streams" +"</li>" +\
                "<li>" + "On the _site_name request stream" +"</li>" +\
                "</ol>")
#        elif selected_type == "article":
#            if content.get("parent"):
    confirm_title = _("Once you share this story, it will:")
    confirm_message = _("<ol>" +\
                    "<li>" + "Be sent directly to %s" + "</li>" +\
                    "<li>" + "Be listed as a response against the request" + "</li>" +\
                    "<li>" + "Appear in your followers' notification streams" + "</li>" +\
                    "</ol>")
#            else:
    confirm_title = _("Once you post this story:")
    confirm_message = _("<ol>" +\
                    "<li>" + "It will appear in your followers' notification streams." + "</li>" +\
                    "<li>" + "You will also be able to share it on Facebook, LinkedIn and Twitter once you post." + "</li>" +\
                    "</ol>")

%>
