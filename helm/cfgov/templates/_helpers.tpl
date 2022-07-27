{{/*
Expand the name of the chart.
*/}}
{{- define "cfgov.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "cfgov.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "cfgov.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "cfgov.labels" -}}
helm.sh/chart: {{ include "cfgov.chart" . }}
{{ include "cfgov.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "cfgov.selectorLabels" -}}
app.kubernetes.io/name: {{ include "cfgov.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Docs Common labels
*/}}
{{- define "cfgov.docs.labels" -}}
helm.sh/chart: {{ include "cfgov.chart" . }}
{{ include "cfgov.docs.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Docs Selector labels
*/}}
{{- define "cfgov.docs.selectorLabels" -}}
app.kubernetes.io/name: {{ include "cfgov.name" . }}-docs
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "cfgov.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "cfgov.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Postgres Environment Vars
*/}}
{{- define "cfgov.postgresEnv" -}}
{{- if .Values.postgresql.enabled -}}
- name: PGUSER
  value: "{{ include "postgresql.username" .Subcharts.postgresql | default "postgres"  }}"
- name: PGPASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ include "postgresql.secretName" .Subcharts.postgresql }}
      key: {{ include "postgresql.userPasswordKey" .Subcharts.postgresql }}
- name: PGHOST
  value: "{{ include "postgresql.primary.fullname" .Subcharts.postgresql | trunc 63 | trimSuffix "-" }}"
- name: PGDATABASE
  value: "{{ include "postgresql.database" .Subcharts.postgresql | default "postgres" }}"
- name: PGPORT
  value: "{{ include "postgresql.service.port" .Subcharts.postgresql }}"
{{- end }}
{{- end }}

{{/*
Mapping/Ingress Hostname FQDN
*/}}
{{- define "cfgov.fqdn" -}}
{{- if .Values.fqdnOverride }}
{{- .Values.fqdnOverride }}
{{- else }}
{{- include "cfgov.fullname" . }}-eks.{{ default "dev-internal" .Values.environmentName }}.aws.cfpb.gov
{{- end }}
{{- end }}
