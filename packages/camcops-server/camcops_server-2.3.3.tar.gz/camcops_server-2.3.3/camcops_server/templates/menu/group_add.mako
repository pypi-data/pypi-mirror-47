## group_add.mako
<%inherit file="base_web_form.mako"/>

<%include file="db_user_info.mako"/>

<h1>${_("Add group")}</h1>

<div class="important">${_("Once created, you can set the group’s description/permissions.")}</div>

${ form }

<%include file="to_main_menu.mako"/>
