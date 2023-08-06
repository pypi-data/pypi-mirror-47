## patient_delete_choose.mako
<%inherit file="base_web_form.mako"/>

<%include file="db_user_info.mako"/>

<h1>${_("Delete patient entirely")}</h1>

<div class="warning">
    ${_("This operation is irrevocable!")}
</div>
<div class="warning">
    ${_("IT WILL PERMANENTLY DELETE THE PATIENT AND ALL ASSOCIATED TASKS from the group that you specify.")}
</div>
<div class="warning">
    ${_("Choose a patient by ID number, and then you’ll be shown a list of tasks that will be deleted if you proceed, and asked to confirm.")}
</div>

${ form }

<%include file="to_main_menu.mako"/>
