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
{{- else }}
{{- if .Values.postgresql.auth.createSecret -}}
- name: PGUSER
  valueFrom:
    secretKeyRef:
      name: {{ include "cfgov.fullname" . }}-postgres
      key: username
- name: PGPASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ include "cfgov.fullname" . }}-postgres
      key: password
- name: PGDATABASE
  valueFrom:
    secretKeyRef:
      name: {{ include "cfgov.fullname" . }}-postgres
      key: database
{{- else }}
- name: PGUSER
  value: "{{ .Values.postgresql.auth.username | default "postgres" }}"
- name: PGPASSWORD
  value: {{ .Values.postgresql.auth.password | quote }}
- name: PGDATABASE
  value: "{{ .Values.postgresql.auth.database | default "postgres" }}"
{{- end }}
- name: PGHOST
  value: {{ .Values.postgresql.external.host | quote }}
- name: PGPORT
  value: "{{ .Values.postgresql.external.port | default "5432" }}"
{{- end }}
{{- end }}

{{/*
Elasticsearch Environment Vars
*/}}
{{- define "cfgov.elasticsearchEnv" -}}
- name: ES_SCHEMA
  value: "{{ default "http" .Values.elasticsearch.protocol }}"
- name: ES_HOST
{{- if .Values.elasticsearch.enabled }}
{{- if eq .Values.elasticsearch.nodeGroup "master" }}
  value: "{{ include "elasticsearch.masterService" .Subcharts.elasticsearch | trunc 63 | trimSuffix "-" }}"
{{- else }}
  value: "{{ include "elasticsearch.uname" .Subcharts.elasticsearch | trunc 63 | trimSuffix "-" }}"
{{- end }}
{{- else }}
  value: "{{ default "elasticsearch-master" .Values.elasticsearch.externalHostname }}"
{{- end }}
- name: ES_PORT
  value: "{{ default "9200" .Values.elasticsearch.httpPort }}"
{{- end }}


{{/*
Opensearch Environment Vars
*/}}
{{- define "cfgov.opensearchEnv" -}}
- name: ES_SCHEMA
  value: "{{ default "https" .Values.opensearch.protocol }}"
- name: ES_HOST
{{- if .Values.opensearch.nameOverride }}
  value: "{{ .Values.opensearch.nameOverride }}-master"
{{- else if .Values.opensearch.fullnameOverride }}
  value: {{ .Values.opensearch.fullnameOverride | quote }}
{{- else }}
  value: opensearch-cluster-master
{{- end }}
- name: ES_PORT
  value: {{ .Values.opensearch.httpPort }}
{{- end }}

{{- define "cfgov.searchEnv" -}}
{{- if .Values.elasticsearch.enabled }}
{{- include "cfgov.elasticsearchEnv" . }}
{{- else if .Values.opensearch.enabled }}
{{- include "cfgov.opensearchEnv" . }}
{{- else }}
- name: ES_SCHEMA
  value: "{{ default "http" .Values.search.schema }}"
- name: ES_HOST
  value: "{{ .Values.search.host }}"
- name: ES_PORT
  value: "{{ default "9200" .Values.search.port }}"
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
