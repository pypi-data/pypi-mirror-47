## audit_trail_choices.mako
<%inherit file="base_web_form.mako"/>

<%include file="db_user_info.mako"/>

<h1>${_("View audit trail (starting with most recent)")}</h1>

<p>${_("Values below are optional.")}</p>

${form}

<%include file="to_main_menu.mako"/>
