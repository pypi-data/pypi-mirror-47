## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="context_menu_items()"></%def>

<%def name="object_helpers()"></%def>

<%def name="render_form_buttons()"></%def>

<%def name="render_form()">
  ${form.render(buttons=capture(self.render_form_buttons))|n}
</%def>

<%def name="render_form_complete()">
  <div style="display: flex; justify-content: space-between;">

    <div class="form-wrapper">
      ${self.render_form()}
    </div>

    <div style="display: flex; align-items: flex-start;">
      <div class="object-helpers">
        ${self.object_helpers()}
      </div>

      <ul id="context-menu">
        ${self.context_menu_items()}
      </ul>
    </div>

  </div>
</%def>

<%def name="modify_tailbone_form()">
  ## NOTE: if you override this, must use <script> tags
</%def>

<%def name="make_tailbone_form_app()">
  ${self.modify_tailbone_form()}
  <script type="text/javascript">

    TailboneForm.data = function() { return TailboneFormData }

    Vue.component('tailbone-form', TailboneForm)

    new Vue({
        el: '#tailbone-form-app'
    })

  </script>
</%def>


${self.render_form_complete()}

% if form.use_buefy:
    ${self.make_tailbone_form_app()}
% endif
