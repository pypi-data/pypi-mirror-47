## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if not use_buefy:
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.batch.js') + '?ver={}'.format(tailbone.__version__))}
  <script type="text/javascript">

    var has_execution_options = ${'true' if master.has_execution_options(batch) else 'false'};

    $(function() {
        % if master.has_worksheet:
            $('.load-worksheet').click(function() {
                disable_button(this);
                location.href = '${url('{}.worksheet'.format(route_prefix), uuid=batch.uuid)}';
            });
        % endif
        % if master.batch_refreshable(batch) and request.has_perm('{}.refresh'.format(permission_prefix)):
            $('#refresh-data').click(function() {
                $(this)
                    .button('option', 'disabled', true)
                    .button('option', 'label', "Working, please wait...");
                location.href = '${url('{}.refresh'.format(route_prefix), uuid=batch.uuid)}';
            });
        % endif
    });

  </script>
  % endif
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">

    .grid-wrapper {
        margin-top: 10px;
    }

    .complete form {
        display: inline;
    }
    
  </style>
</%def>

<%def name="buttons()">
    <div class="buttons">
      ${self.leading_buttons()}
      ${refresh_button()}
      ${execute_button()}
    </div>
</%def>

<%def name="leading_buttons()">
  % if master.has_worksheet and master.allow_worksheet(batch) and request.has_perm('{}.worksheet'.format(permission_prefix)):
      <button type="button" class="load-worksheet">Edit as Worksheet</button>
  % endif
</%def>

<%def name="refresh_button()">
  % if master.batch_refreshable(batch) and request.has_perm('{}.refresh'.format(permission_prefix)):
      % if use_buefy:
          ## TODO: this should surely use a POST request?
          <once-button tag="a"
                       href="${url('{}.refresh'.format(route_prefix), uuid=batch.uuid)}"
                       text="Refresh Data">
          </once-button>
      % else:
          <button type="button" class="button" id="refresh-data">Refresh Data</button>
      % endif
  % endif
</%def>

<%def name="execute_submit_button()">
  <once-button type="is-primary"
               native-type="submit"
               % if not execute_enabled:
               disabled
               % endif
               % if why_not_execute:
               title="${why_not_execute}"
               % endif
               text="${execute_title}">
  </once-button>
</%def>

<%def name="execute_button()">
  % if not batch.executed and request.has_perm('{}.execute'.format(permission_prefix)):

      % if use_buefy:
          % if master.has_execution_options(batch):
              ## TODO: this doesn't work yet
              ${execute_submit_button()}
          % else:
              ${execute_form.render_deform(buttons=capture(execute_submit_button))|n}
          % endif

      % else:
          ## no buefy, do legacy thing
          <button type="button"
                  class="button is-primary"
                  id="execute-batch"
                  % if not execute_enabled:
                  disabled="disabled"
                  % endif
                  % if why_not_execute:
                  title="${why_not_execute}"
                  % endif
                  >
            ${execute_title}
          </button>
      % endif
  % endif

</%def>

<%def name="object_helpers()">
  ${self.render_status_breakdown()}
</%def>

<%def name="render_status_breakdown()">
  % if status_breakdown is not Undefined and status_breakdown is not None:
      <div class="object-helper">
        <h3>Row Status Breakdown</h3>
        <div class="object-helper-content">
          % if status_breakdown:
              <div class="grid full">
                <table>
                  % for i, (status, count) in enumerate(status_breakdown):
                      <tr class="${'even' if i % 2 == 0 else 'odd'}">
                        <td>${status}</td>
                        <td>${count}</td>
                      </tr>
                  % endfor
                </table>
              </div>
          % else:
              <p>Nothing to report yet.</p>
          % endif
        </div>
      </div>
  % endif
</%def>

<%def name="render_form()">
  ## TODO: should use self.render_form_buttons()
  ## ${form.render(form_id='batch-form', buttons=capture(self.render_form_buttons))|n}
  ${form.render(form_id='batch-form', buttons=capture(buttons))|n}
</%def>


${self.render_form_complete()}

% if use_buefy:
    <br /><br />
    ## TODO: stop using |n filter
    ${rows_grid.render_buefy(allow_save_defaults=False, tools=rows_grid_tools)|n}
    ${self.make_tailbone_form_app()}
    ${self.make_tailbone_grid_app()}
% else:
    ## no buefy, so do the traditional thing
    ${rows_grid|n}
% endif

% if not use_buefy and master.handler.executable(batch) and not batch.executed:
    <div id="execution-options-dialog" style="display: none;">
      ${execute_form.render_deform(form_kwargs={'name': 'batch-execution'}, buttons=False)|n}
    </div>
% endif
