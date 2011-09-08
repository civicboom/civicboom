<%inherit file="../../base_email.mako"/>

<%def name="body()">

<h1>Hey Admins!</h1>
<br />
<p>
    Something seems to have failed while a customer was regrading their account, could you check it out for them and let them know what's up!
</p>
<p>
    This is the message I got from the regrade function:<br />
    ${extra_error}
</p>
<p>
    Here are some details of the account:<br />
    Regrading to:       ${new_account_type}<br />
    Name / Username:    ${persona.name} / ${persona.username}<br />
    Email address:      ${persona.email}<br />
    % if persona.payment_account:
        <% pa = persona.payment_account %>
        Payment Account id: ${pa.id}<br />
        Name:               ${pa.name}<br />
        Billing Status:     ${pa.billing_status}<br />
        Start / Freq.:      ${pa.start_date} / ${pa.frequency}<br />
    % else:
        Strange, the persona does not have a payment account :S<br />
    % endif
</p>

<p>Happy booming!</p>
<br />

${self.footer()}
</%def>
