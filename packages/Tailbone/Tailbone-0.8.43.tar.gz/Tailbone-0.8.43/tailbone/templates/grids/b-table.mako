## -*- coding: utf-8; -*-
<b-table
   :data="${data_prop}"
   icon-pack="fas"
   striped
   hoverable
   narrowed>

  <template slot-scope="props">
    % for column in grid_columns:
        <b-table-column field="${column['field']}" label="${column['label']}" ${'sortable' if column['sortable'] else ''}>
          % if grid.is_linked(column['field']):
              <a :href="props.row._action_url_view" v-html="props.row.${column['field']}"></a>
          % else:
              <span v-html="props.row.${column['field']}"></span>
          % endif
        </b-table-column>
    % endfor

    % if grid.main_actions or grid.more_actions:
        <b-table-column field="actions" label="Actions">
          % for action in grid.main_actions:
              <a :href="props.row._action_url_${action.key}"
                 % if action.click_handler:
                 @click.prevent="${action.click_handler}"
                 % endif
                 >
                <i class="fas fa-${action.icon}"></i>
                ${action.label}
              </a>
              &nbsp;
          % endfor
        </b-table-column>
    % endif
  </template>

  <template slot="empty">
    <section class="section">
      <div class="content has-text-grey has-text-centered">
        <p>
          <b-icon
             pack="fas"
             icon="fas fa-sad-tear"
             size="is-large">
          </b-icon>
        </p>
        <p>Nothing here.</p>
      </div>
    </section>
  </template>

</b-table>
