## clinician.mako
<%page args="task: Task"/>

<div class="clinician">
    <table class="taskdetail">
        <tr>
            <td width="50%">${_("Clinician’s specialty:")}</td>
            <td width="50%"><b>${ task.clinician_specialty | h }</b></td>
        </tr>
        <tr>
            <td>${_("Clinician’s name:")}</td>
            <td><b>${ task.clinician_name | h }</b></td>
        </tr>
        <tr>
            <td>${_("Clinician’s professional registration:")}</td>
            <td><b>${ task.clinician_professional_registration | h }</b></td>
        </tr>
        <tr>
            <td>${_("Clinician’s post:")}</td>
            <td><b>${ task.clinician_post | h }</b></td>
        </tr>
        <tr>
            <td>${_("Clinician’s service:")}</td>
            <td><b>${ task.clinician_service | h }</b></td>
        </tr>
        <tr>
            <td>${_("Clinician’s contact details:")}</td>
            <td><b>${ task.clinician_contact_details | h }</b></td>
        </tr>
    </table>
</div>
