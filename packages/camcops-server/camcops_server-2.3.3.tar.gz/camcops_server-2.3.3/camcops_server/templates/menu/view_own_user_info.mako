## view_own_user_info.mako
## <%page args="user: User"/>
<%inherit file="base_web.mako"/>

<%include file="db_user_info.mako"/>

<h1>${_("Information about user")} ${ user.username | h }</h1>

<%include file="user_info_detail.mako" args="user=user"/>

<h1>${_("Groups that user")} ${ user.username | h } ${_("is a member of")}</h1>

<%include file="groups_table.mako" args="groups_page=groups_page, valid_which_idnums=valid_which_idnums, with_edit=False"/>

<%include file="to_main_menu.mako"/>
