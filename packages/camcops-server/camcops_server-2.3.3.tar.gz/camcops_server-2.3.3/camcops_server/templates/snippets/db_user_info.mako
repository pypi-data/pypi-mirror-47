## db_user_info.mako
<%page args="offer_main_menu=False"/>

<% _ = request.gettext %>

<div>
    ${_("Database")}: <b>${ request.database_title | h }</b>.
    %if request.camcops_session.username:
        ${_("Logged in as")} <b>${request.camcops_session.username | h}</b>.
    %endif
    %if offer_main_menu:
        <%include file="to_main_menu.mako"/>
    %endif
</div>
