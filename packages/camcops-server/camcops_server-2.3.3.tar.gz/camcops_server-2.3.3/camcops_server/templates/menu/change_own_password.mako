## change_own_password.mako
<%inherit file="base_web_form.mako"/>

<%include file="db_user_info.mako"/>

%if expired:
    <div class="important">
        ${_("Your password has expired and must be changed.")}
    </div>
%endif

<h1>${_("Change your password")}</h1>

${form}

<div>
    ${_("Minimum password length is ${min_pw_length} characters.")}
</div>
