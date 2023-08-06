## -*- coding: utf-8; -*-
<%inherit file="/form.mako" />

<%def name="title()">Clone ${model_title}: ${instance_title}</%def>

<%def name="render_buefy_form()">
  <br />
  % if use_buefy:
      <b-notification :closable="false">
        You are about to clone the following ${model_title} as a new record:
      </b-notification>
  % else:
  <p>You are about to clone the following ${model_title} as a new record:</p>
  % endif

  ${parent.render_buefy_form()}
</%def>

<%def name="render_form_buttons()">
  <br />
  % if use_buefy:
      <b-notification :closable="false">
        Are you sure about this?
      </b-notification>
  % else:
  <p>Are you sure about this?</p>
  % endif
  <br />

  ${h.form(request.current_route_url(), class_=None if use_buefy else 'autodisable')}
  ${h.csrf_token(request)}
  ${h.hidden('clone', value='clone')}
    <div class="buttons">
      % if use_buefy:
          <once-button tag="a" href="${form.cancel_url}"
                       text="Whoops, nevermind...">
          </once-button>
          <once-button type="is-primary"
                       native-type="submit"
                       text="Yes, please clone away">
          </once-button>
      % else:
          ${h.link_to("Whoops, nevermind...", form.cancel_url, class_='button autodisable')}
          ${h.submit('submit', "Yes, please clone away")}
      % endif
    </div>
  ${h.end_form()}
</%def>


${parent.body()}
