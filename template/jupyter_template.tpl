{% extends 'markdown.tpl'%}

{% block header %}
{% endblock header %}

{% block markdowncell%}
{{cell.source}}
{% endblock markdowncell%}

{% block in_prompt %}
{% if cell.execution_count > 0%}
#### [{{ cell.execution_count if cell.execution_count else ' ' }}]:
{% endif %}
{% endblock in_prompt %}

{% block stream %}
:::message{{"\n"}}
{{- output.text|replace("^    ","") -}}
:::
{% endblock stream %}

{% block execute_result%}
:::message
{{- output.text|replace("^    ","") -}}  
:::

{% endblock execute_result%}
{% block error %}
:::message alert
{{- output.text|replace("^    ","") -}}
:::
{% endblock error %}
