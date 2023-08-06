## -*- coding: utf-8; -*-
<%inherit file="/form.mako" />

<%def name="title()">Temperature Graph</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.bundle.min.js"></script>
  % if not use_buefy:
  <script type="text/javascript">

    var ctx = null;
    var chart = null;

    function fetchReadings(timeRange) {
        if (timeRange === undefined) {
            timeRange = $('#time-range').val();
        }

        var timeUnit;
        if (timeRange == 'last hour') {
            timeUnit = 'minute';
        } else if (['last 6 hours', 'last day'].includes(timeRange)) {
            timeUnit = 'hour';
        } else {
            timeUnit = 'day';
        }

        $('.form-wrapper').mask("Fetching data");
        if (chart) {
            chart.destroy();
        }

        $.get('${url('{}.graph_readings'.format(route_prefix), uuid=probe.uuid)}', {'time-range': timeRange}, function(data) {

            chart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: "${probe.description}",
                        data: data
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            type: 'time',
                            time: {unit: timeUnit},
                            position: 'bottom'
                        }]
                    }
                }
            });

            $('.form-wrapper').unmask();
        });
    }

    $(function() {

        ctx = $('#tempchart');

        $('#time-range').selectmenu({
            change: function(event, ui) {
                fetchReadings(ui.item.value);
            }
        });

        fetchReadings();
    });

  </script>
  % endif
</%def>

<%def name="render_form_complete()">
  % if use_buefy:

      <script type="text/x-template" id="form-page-template">
        <div>

          <div style="display: flex; justify-content: space-between;">

            <div class="form-wrapper">
              <div class="form">

                <b-field horizontal
                         label="Appliance">
                  <div>
                    % if probe.appliance:
                        <a href="${url('tempmon.appliances.view', uuid=probe.appliance.uuid)}">${probe.appliance}</a>
                    % endif
                  </div>
                </b-field>

                <b-field horizontal
                         label="Probe Location">
                  <div>
                    ${probe.location or ""}
                  </div>
                </b-field>

                <b-field horizontal
                         label="Showing">
                  ${time_range}
                </b-field>

              </div>
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

          <canvas ref="tempchart" width="400" height="150"></canvas>
        </div>
      </script>

      <div id="form-page-app">
        <form-page></form-page>
      </div>

  % else:
      ## legacy / not buefy

<div class="form-wrapper">

  <div class="field-wrapper">
    <label>Appliance</label>
    <div class="field">
      % if probe.appliance:
          <a href="${url('tempmon.appliances.view', uuid=probe.appliance.uuid)}">${probe.appliance}</a>
      % endif
    </div>
  </div>

  <div class="field-wrapper">
    <label>Probe Location</label>
    <div class="field">${probe.location or ""}</div>
  </div>

  <div class="field-wrapper">
    <label>Showing</label>
    <div class="field">
      ${time_range}
    </div>
  </div>

</div>

<canvas id="tempchart" width="400" height="150"></canvas>
  % endif
</%def>

<%def name="modify_tailbone_form()">
  <script type="text/javascript">

    FormPage.data = function() { return {
        currentTimeRange: ${json.dumps(current_time_range)|n},
        chart: null,
    }}

    FormPage.methods.fetchReadings = function(timeRange) {

        if (timeRange === undefined) {
            timeRange = this.currentTimeRange
        }

        let timeUnit = null
        if (timeRange == 'last hour') {
            timeUnit = 'minute'
        } else if (['last 6 hours', 'last day'].includes(timeRange)) {
            timeUnit = 'hour'
        } else {
            timeUnit = 'day'
        }

        if (this.chart) {
            this.chart.destroy()
        }

        this.$http.get('${url('{}.graph_readings'.format(route_prefix), uuid=probe.uuid)}', {params: {'time-range': timeRange}}).then(({ data }) => {

            this.chart = new Chart(this.$refs.tempchart, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: "${probe.description}",
                        data: data
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            type: 'time',
                            time: {unit: timeUnit},
                            position: 'bottom'
                        }]
                    }
                }
            });

        })
    }

    FormPage.methods.timeRangeChanged = function(value) {
        this.fetchReadings(value)
    }

    FormPage.mounted = function() {
        this.fetchReadings()
    }

  </script>
</%def>


${parent.body()}
