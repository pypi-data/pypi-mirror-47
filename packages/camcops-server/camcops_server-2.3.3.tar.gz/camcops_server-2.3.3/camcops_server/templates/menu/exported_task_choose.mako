## exported_task_choose.mako
<%inherit file="base_web_form.mako"/>

<%include file="db_user_info.mako"/>

<h1>${_("View export log (starting with most recent)")}</h1>

${form}

<%include file="to_main_menu.mako"/>
