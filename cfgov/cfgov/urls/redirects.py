from django.conf import settings

from cfgov.urls.redirect_helpers import perm, temp


# Redirect all requests under /f/ to the public-facing S3 domain,
# usually files.consumerfinance.gov.
temp(r"f/(.*)", f"https://{settings.AWS_S3_CUSTOM_DOMAIN}" + "/f/$1")

# DO NOT REMOVE. Redirect to auto-create vanity URLs for Payments to Harmed Consumers
perm(
    r"payments/(.*)",
    "/enforcement/payments-harmed-consumers/payments-by-case/$1",
)

# Permanent redirects that exceed Wagtail's 255-character limit for fields
perm(
    r"askcfpb/194/i-used-the-title-services-and-lenders-title-insurance-companies-or-owners-title-insurance-company-listed-by-my-lender-on-my-gfe-but-was-charged-more-than-10-percent-more-than-my-gfe-said-i-would-be-now-my-lender-wont-pay-me-back-what-can-i-do.html",
    "/ask-cfpb/can-my-final-mortgage-costs-increase-from-what-was-on-my-loan-estimate-en-172/",
)
perm(
    r"askcfpb/191/my-lender-or-broker-gave-me-a-gfe-for-15-year-loan-but-when-i-got-to-the-closing-the-documents-said-it-was-a-30-year-loan-my-lender-or-broker-said-not-to-worry-i-can-refinance-later-but-thats-not-in-any-of-my-paperwork-and-i-dont-want-to-close-a-loan-whos.html",
    "/ask-cfpb/my-rate-or-the-fees-changed-between-my-loan-estimate-and-my-closing-disclosure-what-do-i-do-en-184/",
)
perm(
    r"es/obtener-respuestas/c/comprar-una-casa/194/yo-use-los-servicios-del-titulo-y-las-companias-de-titulo-seguro-del-prestamista-o-la-compania-de-seguros-del-titulo-del-propietario-imprimidos-por-mi-prestamista-en-el-gfe-pero-me-cobraron-10-por-ciento-mas-de-lo-que-el-gfe-se-decia-ahora-el-prestamista-.html",
    "/es/obtener-respuestas/pueden-mis-costos-hipotecarios-aumentar-por-encima-de-lo-que-consta-en-el-calculo-del-prestamo-es-172/",
)
perm(
    r"es/obtener-respuestas/c/comprar-una-casa/191/mi-prestamista-o-corredor-me-dio-un-gfe-para-un-prestamo-a-15-anos-pero-al-cierre-los-documentos-decian-que-era-un-prestamo-a-30-anos-mi-prestamista-o-corredor-dijo-que-no-me-preocupara-que-puedo-refinanciar-mas-tarde-pero-eso-no-esta-en-mis-documentos-y-.html",
    "/es/obtener-respuestas/la-tasa-de-interes-o-los-cargos-estipulados-en-la-declaracion-del-cierre-no-son-los-mismos-que-aparecian-en-mi-estimacion-del-prestamo-que-debo-hacer-es-184/",
)
perm(
    r"es/obtener-respuestas/c/comprar-un-vehiculo/879/pase-5-horas-en-el-concesionario-comprando-un-automovil-y-obteniendo-lo-que-pense-que-era-una-buena-tasa-de-interes-finalmente-el-dealer-dijo-vaya-y-llevese-el-automovil-terminaremos-el-financiamiento-mas-tarde-al-dia-siguiente-p-recibi-una-llamada-del-co.html",
    "/es/obtener-respuestas/puede-el-concesionario-aumentar-la-tasa-de-interes-despues-de-que-me-lleve-el-vehiculo-es-831/",
)
perm(
    r"es/obtener-respuestas/c/comprar-un-vehiculo/1175/acabo-de-empezar-un-nuevo-negocio-e-intente-obtener-un-prestamo-vehicular-para-mi-empresa-creo-que-el-prestamista-o-el-concesionario-me-discrimino-y-a-mi-empresa-tambien-cuales-son-los-derechos-que-me-otorga-la-ley.html",
    "/es/obtener-respuestas/que-debo-hacer-si-creo-que-un-prestamista-o-un-concesionario-discrimino-en-mi-contra-cuando-solicite-un-prestamo-para-auto-por-ejemplo-al-negar-mi-solicitud-o-al-cobrarme-una-tasa-de-interes-mas-alta-es-1171/",
)
perm(
    r"ask-cfpb/i-am-a-servicemember-stationed-in-afghanistan-with-a-mortgage-loan-that-is-currently-covered-under-the-service-members-civil-relief-act-scra-our-bank-is-encouraging-my-spouse-to-refinance-to-an-adjustable-rate-mortgage-our-payment-will-be-s-en-301/",
    "/ask-cfpb/i-am-a-servicemember-on-active-duty-thinking-about-refinancing-or-consolidating-my-existing-debt-what-should-i-watch-out-for-en-2037/",
)
perm(
    r"es/obtener-respuestas/no-encontre-nada-sobre-la-tasa-porcentual-anual-apr-del-prestamo-de-dia-de-pago-ni-sobre-cuando-tendre-que-pagarlo-sino-hasta-despues-de-que-recibi-el-dinero-no-deberian-informarme-estas-cosas-con-antelacion-es-1627/",
    "/es/obtener-respuestas/el-prestamista-de-dia-de-pago-dice-que-mi-prestamo-me-costaria-un-15-por-ciento-pero-los-documentos-del-prestamo-indican-que-la-tasa-efectiva-anual-apr-es-de-casi-400-por-ciento-que-es-la-apr-en-un-prestamo-de-dia-de-pago-y-como-debo-usarl-es-1625/",
)
perm(
    r"es/obtener-respuestas/mi-padremadre-recibio-un-aviso-de-un-cobrador-de-deudas-para-que-pague-una-deuda-que-saque-despues-de-que-me-aliste-en-las-fuerzas-militares-ya-esta-pagada-en-su-totalidad-y-estaba-en-mi-nombre-solamente-quien-me-puede-ayudar-para-que-dejen-es-1497/",
    "/es/obtener-respuestas/soy-un-militar-y-un-cobrador-de-deudas-me-esta-acosando-con-respecto-a-una-deuda-que-no-creo-que-deba-cuales-son-mis-derechos-y-donde-puedo-conseguir-ayuda-es-1495/",
)
perm(
    r"es/obtener-respuestas/estoy-atrasado-unos-pocos-meses-en-el-pago-de-mi-deuda-de-la-tarjeta-de-credito-un-cobrador-de-deudas-llamo-y-me-dijo-que-si-yo-no-pagaba-la-deuda-de-mi-tarjeta-de-credito-en-su-totalidad-haria-que-me-pusieran-una-demanda-judicial-bajo-el-cod-es-1487/",
    "/es/obtener-respuestas/soy-un-militar-y-un-cobrador-de-deudas-me-esta-acosando-con-respecto-a-una-deuda-que-no-creo-que-deba-cuales-son-mis-derechos-y-donde-puedo-conseguir-ayuda-es-1495/",
)
perm(
    r"es/obtener-respuestas/cuando-pago-una-cuenta-en-linea-puede-el-banco-o-la-cooperativa-de-credito-sacar-el-dinero-antes-de-la-fecha-programada-que-el-pago-es-1127/",
    "/es/obtener-respuestas/hice-un-pago-a-traves-del-servicio-de-pago-de-facturas-en-linea-de-mi-banco-o-cooperativa-de-credito-el-pago-llego-despues-de-la-fecha-de-vencimiento-y-me-cobraron-un-cargo-por-demora-cuando-debio-llegar-el-pago-de-mi-factura-es-1125/",
)
perm(
    r"es/obtener-respuestas/soy-integrante-de-las-fuerzas-militares-destinado-a-afganistan-y-tengo-un-prestamo-hipotecario-actualmente-cubierto-por-la-ley-de-ayuda-civil-para-militares-scra-por-sus-siglas-en-ingles-nuestro-banco-recomienda-que-con-mi-conyuge-lo-ref-es-301/",
    "/es/obtener-respuestas/soy-un-militar-en-servicio-activo-y-pienso-refinanciar-o-consolidar-mi-deuda-existente-que-debo-tener-en-cuenta-es-2037/",
)
perm(
    r"es/obtener-respuestas/yo-estaba-en-servicio-militar-activo-y-he-regresado-a-casa-acabo-de-oir-que-pude-haber-obtenido-una-reduccion-en-la-tasa-de-interes-de-mi-tarjeta-de-credito-mientras-estaba-en-servicio-activo-ha-pasado-la-oportunidad-para-esta-reduccion-es-94/",
    "/es/obtener-respuestas/estoy-en-las-fuerzas-armadas-hay-limites-sobre-cuanto-me-pueden-cobrar-por-un-prestamo-como-una-hipteca-prestamos-estudiantiles-prestamos-para-auto-o-por-el-saldo-de-la-tarjeta-de-credito-es-893/",
)
perm(
    r"es/obtener-respuestas/por-que-mi-pago-en-linea-no-fue-acreditado-a-mi-cuenta-el-mismo-dia-que-lo-hice-es-81/",
    "/es/obtener-respuestas/hice-un-pago-a-traves-del-servicio-de-pago-de-facturas-en-linea-de-mi-banco-o-cooperativa-de-credito-el-pago-llego-despues-de-la-fecha-de-vencimiento-y-me-cobraron-un-cargo-por-demora-cuando-debio-llegar-el-pago-de-mi-factura-es-1125/",
)
perm(
    r"es/obtener-respuestas/mi-pago-se-vencia-el-domingo-y-entendi-que-significaba-que-tenia-hasta-el-siguiente-dia-habil-lunes-para-pagar-entre-en-linea-al-sitio-web-del-emisor-de-mi-tarjeta-e-hice-un-pago-el-lunes-pero-me-cobraron-un-recargo-pueden-hacer-eso-es-55/",
    "/es/obtener-respuestas/cuando-se-considera-que-mi-pago-de-tarjeta-de-credito-esta-atrasado-es-79/",
)
perm(
    r"es/obtener-respuestas/acabo-de-iniciar-un-nuevo-negocio-e-intente-obtener-un-prestamo-hipotecario-para-mi-compania-creo-que-el-prestamista-tuvo-un-trato-discriminatorio-en-mi-contra-y-en-contra-de-mi-empresa-que-derechos-tengo-conforme-a-la-ley-es-344/",
    "/es/herramientas-del-consumidor/hipotecas/",
)
perm(
    r"ask-cfpb/i-received-a-check-and-tried-to-cash-it-at-the-bankcredit-union-that-holds-the-account-on-which-the-check-was-written-the-bankcredit-union-wouldnt-cash-the-check-because-they-said-the-account-did-not-have-enough-money-can-a-bank-or-credit-en-939/",
    "/consumer-tools/bank-accounts/",
)
perm(
    r"es/obtener-respuestas/recibi-un-cheque-y-trate-de-cobrarlo-en-el-bancola-cooperativa-de-credito-de-procedencia-se-negaron-a-pagarlo-porque-dijeron-que-la-cuenta-no-tenia-dinero-suficiente-pueden-hacer-eso-es-939/",
    "/es/herramientas-del-consumidor/cuentas-bancarias/",
)
perm(
    r"ask-cfpb/i-agreed-to-allow-my-card-issuer-to-charge-an-overlimit-fee-if-i-exceed-my-credit-limit-i-needed-to-make-a-purchase-that-would-have-put-me-over-my-credit-limit-and-was-prepared-to-pay-the-overlimit-fee-but-the-card-issuer-refused-to-authorize-en-33/",
    "/consumer-tools/credit-cards/",
)
perm(
    r"es/obtener-respuestas/estuve-de-acuerdo-en-permitir-que-el-emisor-de-mi-tarjeta-me-cobre-un-cargo-por-sobregiro-si-yo-me-paso-de-mi-limite-de-credito-necesitaba-hacer-una-compra-que-me-habria-puesto-sobre-mi-limite-de-credito-y-estaba-dispuesto-a-pagar-el-cargo-por-es-33/",
    "/es/herramientas-del-consumidor/tarjetas-de-credito/",
)
perm(
    r"es/obtener-respuestas/soy-el-administrador-de-casos-de-un-joven-en-cuidado-tutelar-que-debo-hacer-si-hay-un-error-en-un-informe-de-credito-o-hay-evidencia-de-robo-de-identidad-de-un-joven-que-se-encuentra-en-cuidado-tutelar-es-1869/",
    "/es/herramientas-del-consumidor/informes-y-puntajes-de-credito/",
)
perm(
    r"es/obtener-respuestas/un-prestamista-hipotecario-me-dio-una-tasa-de-interes-mas-alta-de-la-que-deberia-haber-obtenido-de-acuerdo-con-mi-capacidad-crediticia-que-puedo-hacer-si-creo-que-el-prestamista-ha-discriminado-en-mi-contra-es-343/",
    "/consumer-tools/mortgages/",
)
perm(
    r"es/obtener-respuestas/el-valor-de-mi-vivienda-ha-disminuido-y-recibi-una-orden-permanente-de-cambio-de-estacion-pcs-existe-algun-tipo-de-asistencia-que-me-pueda-ayudar-a-vender-mi-casa-sin-tener-que-deber-dinero-despues-de-venderla-es-308/",
    "/es/obtener-respuestas/si-no-puedo-pagar-mi-hipoteca-que-opciones-tengo-es-268/",
)
perm(
    r"es/obtener-respuestas/estoy-en-las-fuerzas-militares-activo-guardia-reserva-o-soy-un-veterano-y-estoy-pensando-en-comprar-una-vivienda-como-se-si-soy-elegible-para-un-prestamo-garantizado-por-el-departamento-de-asuntos-para-veteranos-es-294/",
    "/es/obtener-respuestas/que-es-un-prestamo-de-la-va-es-113/",
)
perm(
    r"es/obtener-respuestas/soy-un-militar-o-veterano-y-actualmente-tengo-una-hipoteca-convencional-con-una-tasa-ajustable-ahora-que-las-tasas-han-bajado-quisiera-refinanciar-a-una-tasa-fija-mas-baja-seria-yo-elegible-para-un-prestamo-de-va-es-298/",
    "/es/obtener-respuestas/que-es-un-prestamo-de-la-va-es-113/",
)
perm(
    r"es/obtener-respuestas/soy-integrante-de-las-fuerzas-militares-o-veterano-y-tengo-un-certificado-de-elegibilidad-coe-por-sus-siglas-en-ingles-de-la-va-por-que-debo-solicitar-un-prestamo-y-cumplir-los-requisitos-de-un-banco-si-la-va-ya-me-ha-certificado-es-304/",
    "/es/obtener-respuestas/que-es-un-prestamo-de-la-va-es-113/",
)
perm(
    r"es/obtener-respuestas/soy-un-veterano-que-esta-comparando-precios-de-hipotecas-quiero-utilizar-mi-beneficio-de-prestamos-para-la-vivienda-de-la-va-pero-algunos-prestamistas-me-dicen-que-no-ofrecen-esos-prestamos-pueden-hacer-esto-es-2059/",
    "/es/obtener-respuestas/que-es-un-prestamo-de-la-va-es-113/",
)

# Redirects intended to catch sub-pages
perm(r"practitioner-resources/(.*)", "/consumer-tools/educator-tools/$1")
perm(
    r"rules-policy/innovation/(.*)", "/rules-policy/competition-innovation/$1"
)
perm(r"policy-compliance/amicus/(.*)", "/compliance/amicus/$1")
perm(r"policy-compliance/enforcement/(.*)", "/enforcement/$1")
perm(r"policy-compliance/rulemaking/(.*)", "/rules-policy/$1")
perm(r"policy-compliance/guidance/(.*)", "/compliance/$1")
perm(r"owning-a-home/process/(.*)", "/owning-a-home/$1")

# Redirect to temporarily fix iRegs 404s
perm(
    r"rules-policy/regulations/\d{4}/(\d{4}/.*)",
    "/rules-policy/regulations/$1",
)

# eRegs
# See discussion: https://GHE/eregs/eRegs-Notes/issues/2103#issuecomment-149183
temp(
    r"eregulations/(.*)2015-26607_20180101(.*)",
    "/eregulations/$12017-18284_20180101$2",
)

# (english) Ask CFPB no longer has special print pages
perm(r"askcfpb/(\d+)/(.+)\.print.html", "/askcfpb/$1/$2.html")

# Reggie 2.0
perm(
    r"policy-compliance/guidance/(ability-repay-qualified-mortgage-rule/|equal-credit-opportunity-act-valuation-rule/|rural-and-underserved-counties-list/|secure-fair-enforcement-for-mortgage-licensing-act/.*|mortserv/.*)",
    "/compliance/compliance-resources/mortgage-resources/$1",
)
perm(
    r"policy-compliance/guidance/(fair-credit-reporting-act/.*|equal-credit-opportunity-act/.*)",
    "/compliance/compliance-resources/other-applicable-requirements/$1",
)

# 9/30/20 IA work, policy and compliance changes
perm(
    r"policy-compliance/guidance/(other-applicable-requirements/.*|consumer-lending-resources/.*|consumer-cards-resources/.*|deposit-accounts-resources/.*|mortgage-resources/.*)",
    "/compliance/compliance-resources/$1",
)

perm(
    r"the-cfpb-wants-you-to-blow-the-whistle-on-lawbreakers",
    "/blog/the-cfpb-wants-you-to-blow-the-whistle-on-lawbreakers/",
)
perm(
    r"financial-education-for-moms-and-all-women",
    "/blog/financial-education-for-moms-and-all-women/",
)
perm(
    r"know-before-you-owe-help-us-make-your-mortgage-forms-better",
    "/blog/know-before-you-owe-help-us-make-your-mortgage-forms-better/",
)
perm(
    r"know-before-you-owe-designing-a-new-disclosure",
    "/blog/know-before-you-owe-designing-a-new-disclosure/",
)
perm(
    r"independent-research-at-the-cfpb",
    "/blog/independent-research-at-the-cfpb/",
)
perm(r"know-before-you-owe-go", "/blog/know-before-you-owe-go/")
perm(
    r"working-to-give-consumers-the-transparency-they-deserve",
    "/blog/working-to-give-consumers-the-transparency-they-deserve/",
)
perm(r"older-americans-and-the-cfpb", "/blog/older-americans-and-the-cfpb/")
perm(r"remembering", "/blog/remembering/")
perm(
    r"know-before-you-owe-where-did-the-online-participants-come-from",
    "/blog/know-before-you-owe-where-did-the-online-participants-come-from/",
)
perm(
    r"know-before-you-owe-credit-unions-community-banks",
    "/blog/know-before-you-owe-credit-unions-community-banks/",
)
perm(
    r"explainer-what-is-a-nonbank-and-what-makes-one-larger",
    "/blog/explainer-what-is-a-nonbank-and-what-makes-one-larger/",
)
perm(r"13000-lessons-learned", "/blog/13000-lessons-learned/")
perm(
    r"mortgage-disclosure-is-heating-up",
    "/blog/mortgage-disclosure-is-heating-up/",
)
perm(r"know-before-you-owe-were-back", "/blog/know-before-you-owe-were-back/")
perm(
    r"get-ready-to-conquer-your-student-loans",
    "/blog/get-ready-to-conquer-your-student-loans/",
)
perm(
    r"reaching-out-for-input-help-us-define-larger-participants",
    "/blog/reaching-out-for-input-help-us-define-larger-participants/",
)
perm(
    r"the-cfpb-and-jags-partnering-to-protect-servicemembers",
    "/blog/the-cfpb-and-jags-partnering-to-protect-servicemembers/",
)
perm(
    r"making-a-difference-in-the-lives-of-immigrants-and-others-who-send-money-abroad",
    "/blog/making-a-difference-in-the-lives-of-immigrants-and-others-who-send-money-abroad/",
)
perm(
    r"joining-the-financial-literacy-and-education-commission",
    "/blog/joining-the-financial-literacy-and-education-commission/",
)
perm(
    r"a-model-form-for-mortgage-statements",
    "/blog/a-model-form-for-mortgage-statements/",
)
perm(r"vita", "/blog/vita/")
perm(r"save-the-date-new-york", "/blog/save-the-date-new-york/")
perm(
    r"your-thoughts-on-private-student-loans",
    "/blog/your-thoughts-on-private-student-loans/",
)
perm(
    r"five-ways-to-keep-more-of-your-tax-refund",
    "/blog/five-ways-to-keep-more-of-your-tax-refund/",
)
perm(
    r"your-feedback-on-know-before-you-owe-student-loans",
    "/blog/your-feedback-on-know-before-you-owe-student-loans/",
)
perm(r"oped/(.*)", "/opeds/$1")
perm(
    r"a-new-tool-for-protecting-the-military-community",
    "/blog/a-new-tool-for-protecting-the-military-community/",
)
perm(
    r"know-before-you-owe-something-new-for-the-new-year",
    "/blog/know-before-you-owe-something-new-for-the-new-year/",
)
perm(r"speech/(.*)", "/speeches/$1")
perm(
    r"getting-a-complete-picture-of-the-payday-market",
    "/blog/getting-a-complete-picture-of-the-payday-market/",
)
perm(
    r"hearing-your-stories-on-payday-lending",
    "/blog/hearing-your-stories-on-payday-lending/",
)
perm(
    r"fulfilling-our-commitment-to-diversity",
    "/blog/fulfilling-our-commitment-to-diversity/",
)
perm(
    r"the-cfpb-launches-its-nonbank-supervision-program",
    "/blog/the-cfpb-launches-its-nonbank-supervision-program/",
)
perm(
    r"a-video-message-from-rich-cordray",
    "/blog/a-video-message-from-rich-cordray/",
)
perm(
    r"cfpb-mortgage-complaint-system-is-up-and-running",
    "/blog/cfpb-mortgage-complaint-system-is-up-and-running/",
)
perm(r"standing-up-for-consumers", "/blog/standing-up-for-consumers/")
perm(r"destination-portland-me-2", "/blog/destination-portland-me-2/")
perm(r"financial-fitness-forum", "/blog/financial-fitness-forum/")
perm(
    r"a-conversation-with-the-south-florida-latino-community",
    "/blog/a-conversation-with-the-south-florida-latino-community/",
)
perm(
    r"the-cfpb-wants-you-to-blow-the-whistle-on-lawbreakers",
    "/blog/the-cfpb-wants-you-to-blow-the-whistle-on-lawbreakers/",
)
perm(
    r"addressing-credit-discrimination",
    "/blog/addressing-credit-discrimination/",
)
perm(
    r"know-before-you-owe-closer-to-closing-mortgage-disclosure-that-is",
    "/blog/know-before-you-owe-closer-to-closing-mortgage-disclosure-that-is/",
)
perm(
    r"live-holly-petraeus-kicks-off-our-financial-fitness-forum",
    "/blog/live-holly-petraeus-kicks-off-our-financial-fitness-forum/",
)
perm(
    r"the-cfpb-ombudsmans-office-an-independent-impartial-confidential-resource",
    "/blog/the-cfpb-ombudsmans-office-an-independent-impartial-confidential-resource/",
)
perm(
    r"how-do-i-shop-for-a-credit-card",
    "/blog/how-do-i-shop-for-a-credit-card/",
)
perm(
    r"know-before-you-owe-making-credit-card-agreements-readable",
    "/blog/know-before-you-owe-making-credit-card-agreements-readable/",
)
perm(r"live-from-cleveland", "/blog/live-from-cleveland/")
perm(
    r"tips-for-avoiding-mortgage-modification-scams",
    "/blog/tips-for-avoiding-mortgage-modification-scams/",
)
perm(
    r"credit-card-complaints-by-the-numbers",
    "/blog/credit-card-complaints-by-the-numbers/",
)
perm(r"cleveland-save-the-date", "/blog/cleveland-save-the-date/")
perm(r"lessons-from-the-road", "/blog/lessons-from-the-road/")
perm(
    r"chime-in-on-private-student-loans",
    "/blog/chime-in-on-private-student-loans/",
)
perm(r"honoring-veterans", "/blog/honoring-veterans/")
perm(
    r"plan-your-spending-to-avoid-holiday-debt",
    "/blog/plan-your-spending-to-avoid-holiday-debt/",
)
perm(
    r"know-before-you-owe-its-closing-time",
    "/blog/know-before-you-owe-its-closing-time/",
)
perm(
    r"protecting-military-members-from-predatory-lending",
    "/blog/protecting-military-members-from-predatory-lending/",
)
perm(
    r"know-before-you-owe-lets-tackle-student-loans",
    "/blog/know-before-you-owe-lets-tackle-student-loans/",
)
perm(
    r"know-your-student-loan-repayment-options",
    "/blog/know-your-student-loan-repayment-options/",
)
perm(r"live-from-minneapolis", "/blog/live-from-minneapolis/")
perm(r"from-day-one", "/blog/from-day-one/")
perm(
    r"know-before-you-owe-whats-next",
    "/blog/know-before-you-owe-whats-next/",
)
perm(r"guide-cfpb-supervision", "/blog/guide-cfpb-supervision/")
perm(r"were-listening", "/blog/were-listening/")
perm(r"meet-us-in-minnesota", "/blog/meet-us-in-minnesota/")
perm(
    r"help-for-struggling-military-homeowners",
    "/blog/help-for-struggling-military-homeowners/",
)
perm(
    r"seeing-servicemembers-as-dollar-signs-in-uniform",
    "/blog/seeing-servicemembers-as-dollar-signs-in-uniform/",
)
perm(r"lessons-weve-learned", "/blog/lessons-weve-learned/")
perm(r"live-from-philadelphia", "/blog/live-from-philadelphia/")
perm(
    r"the-cfpb-applying-the-lessons-of-the-financial-crisis",
    "/blog/the-cfpb-applying-the-lessons-of-the-financial-crisis/",
)
perm(
    r"know-before-you-owe-and-now-for-something-completely-different",
    "/blog/know-before-you-owe-and-now-for-something-completely-different/",
)
perm(
    r"avoiding-loan-scams-after-a-natural-disaster",
    "/blog/avoiding-loan-scams-after-a-natural-disaster/",
)
perm(r"co-signing-on-campus", "/blog/co-signing-on-campus/")
perm(
    r"coordinating-consumer-complaints",
    "/blog/coordinating-consumer-complaints/",
)
perm(
    r"promoting-openness-in-cfpb-rulemaking",
    "/blog/promoting-openness-in-cfpb-rulemaking/",
)
perm(r"on-our-way", "/blog/on-our-way/")
perm(r"military-advocates-on-duty", "/blog/military-advocates-on-duty/")
perm(
    r"know-before-you-owe-weigh-in-now",
    "/blog/know-before-you-owe-weigh-in-now/",
)
perm(
    r"mortgage-disclosures-are-getting-better-thanks-to-you",
    "/blog/mortgage-disclosures-are-getting-better-thanks-to-you/",
)
perm(
    r"get-and-keep-a-good-credit-score",
    "/blog/get-and-keep-a-good-credit-score/",
)
perm(
    r"preserving-a-level-playing-field-and-access-to-mortgages",
    "/blog/preserving-a-level-playing-field-and-access-to-mortgages/",
)
perm(
    r"a-consumer-centered-supervision-program",
    "/blog/a-consumer-centered-supervision-program/",
)
perm(r"a-strong-foundation", "/blog/a-strong-foundation/")
perm(
    r"cfpb-spending-update-second-quarter-2011",
    "/blog/cfpb-spending-update-second-quarter-2011/",
)
perm(
    r"continuing-our-work-with-community-banks-and-credit-unions",
    "/blog/continuing-our-work-with-community-banks-and-credit-unions/",
)
perm(
    r"talking-to-our-daughters-and-sons-about-personal-finance",
    "/blog/talking-to-our-daughters-and-sons-about-personal-finance/",
)
perm(
    r"consumer-education-and-engagement-at-the-cfpb",
    "/blog/consumer-education-and-engagement-at-the-cfpb/",
)
perm(
    r"national-financial-literacy-month",
    "/blog/national-financial-literacy-month/",
)
perm(r"fulfilling-a-commitment", "/blog/fulfilling-a-commitment/")
perm(r"keeping-it-sunny-at-the-cfpb", "/blog/keeping-it-sunny-at-the-cfpb/")
perm(
    r"cfpb-spending-update-first-quarter-2011",
    "/blog/cfpb-spending-update-first-quarter-2011/",
)
perm(
    r"so-how-do-we-put-elizabeth-warrens-calendar-online",
    "/blog/so-how-do-we-put-elizabeth-warrens-calendar-online/",
)
perm(
    r"be-a-part-of-our-supervision-team",
    "/blog/be-a-part-of-our-supervision-team/",
)
perm(
    r"an-accountable-consumer-bureau",
    "/blog/an-accountable-consumer-bureau/",
)
perm(
    r"the-card-act-conference-what-we-learned",
    "/blog/the-card-act-conference-what-we-learned/",
)
perm(r"its-always-sunny-at-the-cfpb", "/blog/its-always-sunny-at-the-cfpb/")
perm(r"a-new-voice-for-students", "/blog/a-new-voice-for-students/")
perm(
    r"a-ray-of-hope-for-american-consumers",
    "/blog/a-ray-of-hope-for-american-consumers/",
)
perm(
    r"better-together-how-ncpw-partner-agencies-are-protecting-consumers",
    "/blog/better-together-how-ncpw-partner-agencies-are-protecting-consumers/",
)
perm(
    r"december-2010-cfpb-implementation-team-reaches-100-employees",
    "/blog/december-2010-cfpb-implementation-team-reaches-100-employees/",
)
perm(
    r"february-2011-cfpbs-hr-system-comes-online",
    "/blog/february-2011-cfpbs-hr-system-comes-online/",
)
perm(
    r"september-2010-transfer-date-announced",
    "/blog/september-2010-transfer-date-announced/",
)
perm(
    r"open-for-suggestions-our-favorite-videos",
    "/blog/open-for-suggestions-our-favorite-videos/",
)
perm(r"finding-a-home", "/blog/finding-a-home/")
perm(r"the-credit-card-act-turns-one", "/blog/the-credit-card-act-turns-one/")
perm(
    r"asking-the-public-about-the-card-act",
    "/blog/asking-the-public-about-the-card-act/",
)
perm(
    r"professor-warren-speaks-with-americas-credit-unions",
    "/blog/professor-warren-speaks-with-americas-credit-unions/",
)
perm(
    r"talking-to-small-financial-service-providers",
    "/blog/talking-to-small-financial-service-providers/",
)
perm(
    r"at-the-podium-with-americas-credit-unions",
    "/blog/at-the-podium-with-americas-credit-unions/",
)
perm(r"one-teachers-challenge", "/blog/one-teachers-challenge/")
perm(
    r"a-level-playing-field-for-consumer-financial-products-and-services",
    "/blog/a-level-playing-field-for-consumer-financial-products-and-services/",
)
perm(
    r"building-better-consumer-protection",
    "/blog/building-better-consumer-protection/",
)
perm(r"consumer-scams", "/blog/consumer-scams/")
perm(
    r"professor-warren-speaks-to-consumers-union",
    "/blog/professor-warren-speaks-to-consumers-union/",
)
perm(
    r"october-2010-cfpb-implementation-team-moves-into-temporary-headquarters",
    "/blog/october-2010-cfpb-implementation-team-moves-into-temporary-headquarters/",
)
perm(r"the-cfpbs-budget", "/blog/the-cfpbs-budget/")
perm(
    r"february-2011-cfpb-website-launches",
    "/blog/february-2011-cfpb-website-launches/",
)
perm(r"holly-petraeus-testifies", "/blog/holly-petraeus-testifies/")
perm(
    r"calendars-credit-cards-and-consumer-education",
    "/blog/calendars-credit-cards-and-consumer-education/",
)
perm(
    r"the-cfpb-and-the-religious-community",
    "/blog/the-cfpb-and-the-religious-community/",
)
perm(r"robins-story-andrews-story", "/blog/robins-story-andrews-story/")
perm(
    r"responding-to-your-suggestions",
    "/blog/responding-to-your-suggestions/",
)
perm(r"openforsuggestions", "/blog/openforsuggestions/")
perm(r"welcometothewebsite", "/blog/welcometothewebsite/")
perm(r"off-topic-blog-comments", "/blog/off-topic-blog-comments/")
perm(
    r"hearing-directly-from-our-servicemembers",
    "/blog/hearing-directly-from-our-servicemembers/",
)
perm(r"welcominghollypetraeus", "/blog/welcominghollypetraeus/")
perm(
    r"notice-about-possibly-malicious-emails",
    "/blog/notice-about-possibly-malicious-emails/",
)
perm(
    r"set-a-goal-and-start-a-savings-habit",
    "/blog/set-a-goal-and-start-a-savings-habit/",
)
perm(
    r"were-taking-nominations-for-our-consumer-advisory-board",
    "/blog/were-taking-nominations-for-our-consumer-advisory-board/",
)
perm(r"live-from-new-york-city", "/blog/live-from-new-york-city/")
perm(
    r"whats-your-status-when-it-comes-to-overdraft-coverage",
    "/blog/whats-your-status-when-it-comes-to-overdraft-coverage/",
)
perm(
    r"sbrefa-small-providers-and-mortgage-disclosure",
    "/blog/sbrefa-small-providers-and-mortgage-disclosure/",
)
perm(
    r"know-before-you-owe-the-last-dance-or-is-it",
    "/blog/know-before-you-owe-the-last-dance-or-is-it/",
)
perm(
    r"office-of-financial-education-begins-listening-tour-in-new-york",
    "/blog/office-of-financial-education-begins-listening-tour-in-new-york/",
)
perm(
    r"we-want-to-make-it-easier-for-you-to-submit-comments-on-streamlining-regulations",
    "/blog/we-want-to-make-it-easier-for-you-to-submit-comments-on-streamlining-regulations/",
)
perm(
    r"making-a-difference-in-the-lives-of-immigrants-and-others-who-send-money-abroad",
    "/blog/making-a-difference-in-the-lives-of-immigrants-and-others-who-send-money-abroad/",
)
temp(r"hbd", "/about-us/blog/four-years-working-for-you/")
perm(r"studentdebtstress", "/blog/tell-us-about-your-student-debt-stress/")
perm(
    r"managing-someone-elses-money-virginia",
    "/blog/managing-someone-elses-money-virginia/",
)
temp(r"HMDA", "/data-research/hmda/")
perm(
    r"yourstories",
    "/your-story/?utm_source=print&utm_medium=flyer&utm_term=2015&utm_campaign=TaxInsert",
)

# Fix for a typo that went out in an email release
perm(r"project", "/projectcatalyst")

# Know Before You Owe
perm(r"kbyo(.*)", "/know-before-you-owe$1")
perm(r"knowbeforeyouowe(.*)", "/know-before-you-owe$1")
perm(r"(.*)/realestateprofessionals(.*)", "$1/real-estate-professionals$2")
perm(r"real-estate", "/know-before-you-owe/real-estate-professionals/")

# Retirement redirects
perm(
    r"retirement/claiming-social-security",
    "/consumer-tools/retirement/before-you-claim/",
)
perm(
    r"jubilacion",
    "/es/herramientas-del-consumidor/jubilacion/antes-de-solicitar/",
)
perm(r"retirement", "/consumer-tools/retirement/before-you-claim/")

# Redirect from /es/ suffix urls
perm(
    r"consumer-tools/financial-well-being/es/",
    "/es/herramientas-del-consumidor/bienestar-financiero/",
)
perm(
    r"consumer-tools/retirement/before-you-claim/es/",
    "/es/herramientas-del-consumidor/jubilacion/antes-de-solicitar/",
)

# Owning a Home redirects
perm(r"owningahome", "/owning-a-home")
perm(
    r"owning-a-home/monthly-payment-worksheet[/]*",
    "/owning-a-home/resources/monthly_payment_worksheet.pdf",
)

# redirects associated with the v1 project
perm(
    r"leadership-calendar/(?!cfpb-leadership.json)",
    "/about-us/the-bureau/leadership-calendar/",
)
perm(r"jobs/detail/.*", "/careers/current-openings/")
perm(r"jobs/(?!supervision/)", "/about-us/careers/")
perm(r"retirement", "/retirement/before-you-claim")

# Legacy /credit-cards pages
#   Redirect most to data-research
perm(
    r"credit-cards/(?!agreements)(?!credit-card-act)(?!definitions)(?!knowbeforeyouowe)(?!college-agreements).*",
    "/data-research/credit-card-data/",
)
perm(
    r"credit-cards/knowbeforeyouowe",
    "/data-research/credit-card-data/know-you-owe-credit-cards/",
)
perm(
    r"credit-cards/definitions",
    "/data-research/credit-card-data/know-you-owe-credit-cards/credit-card-contract-definitions/",
)
perm(
    r"credit-cards/credit-card-act",
    "/data-research/credit-card-data/",
)
perm(
    r"credit-cards/credit-card-act/card-act-conference-key-findings",
    "/data-research/research-reports/card-act-conference-key-findings/",
)
perm(
    r"credit-cards/credit-card-act/feb2011-factsheet",
    "/data-research/research-reports/card-act-conference-key-findings/",
)

# regulatory-implementation
perm(
    r"regulatory-implementation",
    "/compliance/implementation-guidance/",
)

# misc redirects
perm(r"guidance/supervision/manual/", "/compliance/supervision-examinations/")
perm(r"foia/(?!quarterly)(.*)", "/foia-requests/$1")

# strip pagination from legacy blog and category URL's
perm(r"blog/(.+)/page/(\d+)", "/blog/$1/")

# Legacy blog category URL's
perm(
    r"blog/category/mortgages/.*",
    "/about-us/blog/?filter1_topics=mortgages",
)
perm(
    r"blog/category/mortgages/mortgage-closing-mortgages/.*",
    "/about-us/blog/?filter1_topics=mortgage-closing",
)
perm(
    r"blog/category/mortgages/reverse-mortgages/.*",
    "/about-us/blog/?filter1_topics=reverse-mortgages",
)
perm(
    r"blog/category/students/.*",
    "/about-us/blog/?filter1_topics=students",
)
perm(
    r"blog/category/student-loans/.*",
    "/about-us/blog/?filter1_topics=student-loans",
)
perm(
    r"blog/category/financial-education/.*",
    "/about-us/blog/?filter1_topics=financial-education",
)
perm(
    r"blog/category/servicemembers/.*",
    "/about-us/blog/?filter1_topics=servicemembers",
)
perm(
    r"blog/category/older-americans/.*",
    "/about-us/blog/?filter1_topics=older-americans",
)
perm(
    r"blog/category/featured/.*",
    "/about-us/blog/?filter1_topics=featured",
)
perm(
    r"blog/category/rulemaking/.*",
    "/about-us/blog/?filter1_topics=rulemaking",
)
perm(
    r"blog/category/enforcement/.*",
    "/about-us/blog/?filter1_topics=enforcement",
)
perm(
    r"blog/category/know-before-you-owe/.*",
    "/about-us/blog/?filter1_topics=know-before-you-owe",
)
perm(r"blog/category/video/.*", "/about-us/blog/?filter1_topics=video")
perm(
    r"blog/category/video/livestream/.*",
    "/about-us/blog/?filter1_topics=livestream",
)
perm(
    r"blog/category/credit-cards/.*",
    "/about-us/blog/?filter1_topics=credit-cards",
)
perm(
    r"blog/category/building-the-agency/.*",
    "/about-us/blog/?filter1_topics=about-the-bureau",
)
perm(
    r"blog/category/mortgage-disclosure/.*",
    "/about-us/blog/?filter1_topics=mortgage-disclosure",
)
perm(
    r"blog/category/about-the-bureau/.*",
    "/about-us/blog/?filter1_topics=about-the-bureau",
)
perm(
    r"blog/category/about-the-bureau/technology/.*",
    "/about-us/blog/?filter1_topics=technology",
)
perm(
    r"blog/category/outreach/.*",
    "/about-us/blog/?filter1_topics=outreach",
)
perm(
    r"blog/category/consumer-advisory-board/.*",
    "/about-us/blog/?filter1_topics=consumer-advisory-board",
)
perm(
    r"blog/category/consumer-advisory/.*",
    "/about-us/blog/?filter1_topics=consumer-advisory",
)
perm(
    r"blog/category/consumer-protection/.*",
    "/about-us/blog/?filter1_topics=financial-education",
)
perm(
    r"blog/category/debt-collection-2/.*",
    "/about-us/blog/?filter1_topics=debt-collection",
)
perm(
    r"blog/category/consumer-response/.*",
    "/about-us/blog/?filter1_topics=consumer-response",
)
perm(
    r"blog/category/complaints/.*",
    "/about-us/blog/?filter1_topics=complaints",
)
perm(r"blog/category/consumer-voice/.*", "/about-us/blog/")
perm(
    r"blog/category/bureau-milestones/.*",
    "/about-us/blog/?filter1_topics=bureau-milestones",
)
perm(
    r"blog/category/payday-loans/.*",
    "/about-us/blog/?filter1_topics=payday-loans",
)
perm(
    r"blog/category/financial-empowerment/.*",
    "/about-us/blog/?filter1_topics=financial-empowerment",
)
perm(
    r"blog/category/fair-lending/.*",
    "/about-us/blog/?filter1_topics=fair-lending",
)
perm(
    r"blog/category/open-gov/.*",
    "/about-us/blog/?filter1_topics=open-government",
)
perm(r"blog/category/data/.*", "/about-us/blog/?filter1_topics=data")
perm(
    r"blog/category/research/.*",
    "/about-us/blog/?filter1_topics=research",
)
perm(
    r"blog/category/credit-scores/.*",
    "/about-us/blog/?filter1_topics=credit-reporting",
)
perm(
    r"blog/category/credit-report/.*",
    "/about-us/blog/?filter1_topics=credit-reporting",
)
perm(
    r"blog/category/checking/.*",
    "/about-us/blog/?filter1_topics=checking",
)
perm(
    r"blog/category/save-the-date/.*",
    "/about-us/blog/?filter1_topics=save-the-date",
)
perm(
    r"blog/category/field-hearing/.*",
    "/about-us/blog/?filter1_topics=field-hearing",
)
perm(
    r"blog/category/supervision/.*",
    "/about-us/blog/?filter1_topics=supervision",
)
perm(
    r"blog/category/supervision/nonbanks/.*",
    "/about-us/blog/?filter1_topics=nonbanks",
)
perm(
    r"blog/category/supervision/bank-supervision-supervision/.*",
    "/about-us/blog/?filter1_topics=bank-supervision",
)
perm(
    r"blog/category/remittances/.*",
    "/about-us/blog/?filter1_topics=money-transfers",
)
perm(
    r"blog/category/private-student-loans/.*",
    "/about-us/blog/?filter1_topics=student-loans",
)
perm(r"blog/category/scams/.*", "/about-us/blog/?filter1_topics=scams")
perm(r"blog/category/uncategorized/.*", "/about-us/blog/")
perm(
    r"blog/category/website/.*",
    "/about-us/blog/?filter1_topics=online-resources",
)
perm(
    r"blog/category/national-consumer-protection-week/.*",
    "/about-us/blog/?filter1_topics=national-consumer-protection-week",
)
perm(r"blog/category/parents/.*", "/about-us/blog/?filter1_topics=parents")
perm(
    r"blog/category/everyone-has-a-story/.*",
    "/about-us/blog/?filter1_topics=everyone-has-a-story",
)
perm(
    r"blog/category/consumer-engagement/.*",
    "/about-us/blog/?filter1_topics=consumer-engagement",
)
perm(
    r"blog/category/tell-your-story/.*",
    "/about-us/blog/?filter1_topics=everyone-has-a-story",
)
perm(
    r"blog/category/auto-loans/.*",
    "/about-us/blog/?filter1_topics=auto-loans",
)
perm(
    r"blog/category/credit-unions/.*",
    "/about-us/blog/?filter1_topics=credit-unions",
)
perm(
    r"blog/category/arbitration/.*",
    "/about-us/blog/?filter1_topics=arbitration",
)
perm(r"blog/category/saving/.*", "/about-us/blog/?filter1_topics=saving")
perm(
    r"blog/category/community-banks/.*",
    "/about-us/blog/?filter1_topics=community-banks",
)
perm(
    r"blog/category/open-for-suggestions/.*",
    "/about-us/blog/?filter1_topics=open-for-suggestions",
)
perm(
    r"blog/category/explainer/.*",
    "/about-us/blog/?filter1_topics=explainer",
)
perm(
    r"blog/category/cfpb-ombudsman/.*",
    "/about-us/blog/?filter1_topics=cfpb-ombudsman",
)
perm(r"blog/category/ecoa/.*", "/about-us/blog/?filter1_topics=ecoa")
perm(
    r"blog/category/prepaid-cards/.*",
    "/about-us/blog/?filter1_topics=prepaid-cards",
)
perm(
    r"blog/category/consumer-story/.*",
    "/about-us/blog/?filter1_topics=consumer-story",
)
perm(
    r"blog/category/military/.*",
    "/about-us/blog/?filter1_topics=servicemembers",
)
perm(
    r"blog/category/academic-research-council/.*",
    "/about-us/blog/?filter1_topics=academic-research-council",
)
perm(
    r"blog/category/our-team/.*",
    "/about-us/blog/?filter1_topics=about-the-bureau",
)
perm(
    r"blog/category/credit-card-act/.*",
    "/about-us/blog/?filter1_topics=credit-cards",
)
perm(
    r"blog/category/overdrafts/.*",
    "/about-us/blog/?filter1_topics=overdrafts",
)
perm(r"blog/category/jobs/.*", "/about-us/blog/?filter1_topics=careers")
perm(
    r"blog/category/debit-cards/.*",
    "/about-us/blog/?filter1_topics=debit-cards",
)
perm(
    r"blog/category/project-catalyst/.*",
    "/about-us/blog/?filter1_topics=project-catalyst",
)
perm(r"blog/category/fraud/.*", "/about-us/blog/?filter1_topics=fraud")
perm(
    r"blog/category/foreclosure/.*",
    "/about-us/blog/?filter1_topics=foreclosure",
)
perm(
    r"blog/category/young-americans/.*",
    "/about-us/blog/?filter1_topics=youth",
)
perm(
    r"blog/category/medical-debt/.*",
    "/about-us/blog/?filter1_topics=medical-debt",
)
perm(r"blog/category/youth/.*", "/about-us/blog/?filter1_topics=youth")
perm(
    r"blog/category/financial-literacy-month/.*",
    "/about-us/blog/?filter1_topics=financial-literacy-month",
)
perm(
    r"blog/category/mortgage-closing/.*",
    "/about-us/blog/?filter1_topics=mortgage-closing",
)
perm(
    r"blog/category/regulations/.*",
    "/about-us/blog/?filter1_topics=regulations",
)
perm(
    r"blog/category/community-bank-advisory-council/.*",
    "/about-us/blog/?filter1_topics=community-bank-advisory-council",
)
perm(
    r"blog/category/bank-supervision/.*",
    "/about-us/blog/?filter1_topics=supervision",
)
perm(
    r"blog/category/equal-opportunity/.*",
    "/about-us/blog/?filter1_topics=equal-opportunity",
)
perm(
    r"blog/category/from-the-director/.*",
    "/about-us/blog/?filter1_topics=from-the-director",
)
perm(
    r"blog/category/compliance/.*",
    "/about-us/blog/?filter1_topics=compliance",
)
perm(
    r"blog/category/tribal-governments/.*",
    "/about-us/blog/?filter1_topics=tribal-governments",
)
perm(
    r"blog/category/doing-business-with-us/.*",
    "/about-us/blog/?filter1_topics=procurement",
)
perm(r"blog/category/taxes/.*", "/about-us/blog/?filter1_topics=taxes")
perm(
    r"blog/category/banking-3/.*",
    "/about-us/blog/?filter1_topics=banking",
)
perm(
    r"blog/category/predatory-lending/.*",
    "/about-us/blog/?filter1_topics=student-loans",
)
perm(r"blog/category/mymoney-gov/.*", "/about-us/blog/")
perm(r"blog/category/financial-crisis/.*", "/about-us/blog/")
perm(r"blog/category/speech/.*", "/newsroom/?filter_category=speech")
perm(
    r"blog/category/access-to-finance/.*",
    "/about-us/blog/?filter1_topics=access-to-finance",
)
perm(
    r"blog/category/civil-penalty-fund/.*",
    "/about-us/blog/?filter1_topics=civil-penalty-fund",
)
perm(
    r"blog/category/spanish/.*",
    "/about-us/blog/?filter1_topics=cfpb-en-espanol",
)
perm(r"blog/category/small-business/.*", "/about-us/blog/")
perm(
    r"blog/category/disability/.*",
    "/about-us/blog/?filter1_topics=persons-with-disabilities",
)
perm(
    r"blog/category/this-week/.*",
    "/about-us/blog/?filter1_topics=about-the-bureau",
)
perm(
    r"blog/category/faith-based-community/.*",
    "/about-us/blog/?filter1_topics=outreach",
)
perm(
    r"blog/category/home-equity-loan/.*",
    "/about-us/blog/?filter1_topics=home-equity-loan",
)
perm(r"blog/category/fair-housing-act/.*", "/about-us/blog/")
perm(
    r"blog/category/small-business-review/.*",
    "/about-us/blog/?filter1_topics=small-business-review",
)
perm(r"blog/category/design/.*", "/about-us/blog/?filter1_topics=design")
perm(r"blog/category/partnerships/.*", "/about-us/blog/")
perm(
    r"blog/category/fair-credit-reporting-act/.*",
    "/about-us/blog/?filter1_topics=credit-reporting",
)
perm(
    r"blog/category/consumers-with-disabilities/.*",
    "/about-us/blog/?filter1_topics=persons-with-disabilities",
)
perm(
    r"blog/category/money-transfers/.*",
    "/about-us/blog/?filter1_topics=money-transfers",
)
perm(
    r"blog/category/diversity/.*",
    "/about-us/blog/?filter1_topics=diversity",
)
perm(
    r"blog/category/security/.*",
    "/about-us/blog/?filter1_topics=security",
)
perm(
    r"blog/category/mobile-financial-services/.*",
    "/about-us/blog/?filter1_topics=mobile-financial-services",
)
perm(r"blog/category/equal-credit-opportunity-act/.*", "/about-us/blog/")
perm(
    r"blog/category/fair-debt-collection-practices-act/.*",
    "/about-us/blog/",
)
perm(
    r"blog/category/real-estate-settlement-procedures-act/.*",
    "/about-us/blog/",
)
perm(r"blog/category/truth-in-lending-act/.*", "/about-us/blog/")
perm(
    r"blog/category/virtual-currency/.*",
    "/about-us/blog/?filter1_topics=virtual-currency",
)
perm(
    r"blog/category/equal-treatment/.*",
    "/about-us/blog/?filter1_topics=discrimination",
)

# Redirect old FinEd Resources downloads to their new Wagtail sublanding pages
perm(r"money-as-you-grow/(.*)\.pdf", "/consumer-tools/money-as-you-grow/")
perm(
    r"library-resources/(.*)\.(docx|pdf|png|txt|zip)",
    "/consumer-tools/educator-tools/library-resources/",
)
perm(
    r"tax-preparer-resources/(.*)\.(docx|pdf|png|txt|zip)",
    "/consumer-tools/educator-tools/resources-for-tax-preparers/",
)

# ILSA vanity URL
perm(r"ILSA", "/compliance/interstate-land-sales-registration/")

# Link from payday lending disclosures
perm(
    r"payday",
    "/askcfpb/search/?selected_facets=category_exact:payday-loans",
)

# Link from Meals on Wheels placemats; now with tracking querystring (as of 9/12/2016)
perm(
    r"oa",
    "/askcfpb/1935/how-can-i-protect-myself-and-others-i-care-about-from-fraud-and-scams.html?utm_source=print&utm_medium=placemat&utm_campaign=OAMealsOnWheelsFall2016",
)

# Auto Loans vanity URL
perm(r"auto-?loans?", "/consumer-tools/auto-loans/")

# Elder Abuse short URLs, requested 9/12/2016
perm(
    r"fi_advisory_elderabuse",
    "https://files.consumerfinance.gov/f/201603_cfpb_advisory-for-financial-institutions-on-preventing-and-responding-to-elder-financial-exploitation.pdf",
)
perm(
    r"fi_report_elderabuse",
    "https://files.consumerfinance.gov/f/201603_cfpb_recommendations-and-report-for-financial-institutions-on-preventing-and-responding-to-elder-financial-exploitation.pdf",
)

# Prepaid consumer resource page vanity URL
perm(
    r"prepaids?",
    "/consumer-tools/prepaid-cards/?utm_source=prepaid&utm_medium=redirect&utm_campaign=PrepaidRedirects",
)

# Prepaid disclosure files redirect
perm(
    r"prepaid-?disclosure-?files",
    "https://github.com/cfpb/prepaid-disclosure-files",
)

# Short URL for giving over the phone to callers, requested by CR in Nov. 2016
perm(
    r"CreditReportingDisputeLetter",
    "https://files.consumerfinance.gov/f/documents/092016_cfpb_CreditReportingDisputeLetter.docx",
)

# Money as You Grow
perm(r"parents?", "/consumer-tools/money-as-you-grow/")
perm(
    r"money-?as-?you-?grow(.*)",
    "/consumer-tools/money-as-you-grow$1",
)

# Youth Financial Education
perm(
    r"youth-financial-education",
    "/consumer-tools/educator-tools/youth-financial-education/",
)
perm(
    r"(/consumer-tools/educator-tools/youth-financial-education/curriculum-review/).+",
    "$1",
)
perm(
    r"consumer-tools/educator-tools/youth-financial-education/survey/3-5.*",
    "https://files.consumerfinance.gov/f/documents/cfpb_building_block_activities_youth-financial-capability-survey-elementary_school.pdf",
)
perm(
    r"consumer-tools/educator-tools/youth-financial-education/survey/6-8.*",
    "https://files.consumerfinance.gov/f/documents/cfpb_building_block_activities_youth-financial-capability-survey-middle_school.pdf",
)
perm(
    r"consumer-tools/educator-tools/youth-financial-education/survey/9-12.*",
    "https://files.consumerfinance.gov/f/documents/cfpb_building_blocks_youth-financial-capability-survey-high_school.pdf",
)

# Adult Financial Education
perm(
    r"adult-financial-education",
    "/consumer-tools/educator-tools/adult-financial-education/",
)

# MAYG Spanish, redirecting from the "just add /es" model to the real address
perm(r"money-as-you-grow/es", "/es/el-dinero-mientras-creces/")
perm(
    r"money-as-you-grow/early-childhood/es",
    "/es/el-dinero-mientras-creces/ninez-temprana/",
)
perm(
    r"money-as-you-grow/middle-childhood/es",
    "/es/el-dinero-mientras-creces/ninez-media/",
)
perm(
    r"money-as-you-grow/young-adulthood/es",
    "/es/el-dinero-mientras-creces/la-adolescencia-y-la-juventud/",
)
perm(
    r"money-as-you-grow/how-kids-develop-money-skills/es",
    "/es/el-dinero-mientras-creces/como-los-jovenes-forman-habilidades-financieras/",
)

# "From here to homeowner" roadmap short URLs for printed worksheet, requested 12/13/16
perm(r"mile1", "/owning-a-home/prepare/#credit")
perm(r"mile2", "/owning-a-home/prepare/#price")
perm(r"mile3", "/owning-a-home/explore/")
perm(r"mile4", "/owning-a-home/explore/#preapproval")
perm(r"mile5", "/owning-a-home/explore/#home")
perm(r"mile6", "/owning-a-home/compare/")
perm(r"mile7", "/owning-a-home/compare/#choose")
perm(r"mile8", "/owning-a-home/close/#services")
perm(r"mile9", "/owning-a-home/close/#review")

# We have URLs at the end of sentences on printed material and occasionally people type the period that follows the URL as part of it.
perm(r"(.*)\\.", "/$1")

# Redirects associated with moving Everyone Has a Story to Wagtail
## Redirect URLS in the form of: /yourstory/slug
##                               /yourstory/slug/
##                               /yourstory
##                               /yourstory/
perm(r"yourstory/([^/]+)(/*)", "/consumer-tools/everyone-has-a-story/$1/")
perm(r"yourstory", "/consumer-tools/everyone-has-a-story/")

## Redirect William, who is a special case due to his slug changing
perm(
    r"everyone-has-a-story/william-paying-debts-you-dont-owe/",
    "/consumer-tools/everyone-has-a-story/william-not-my-debt/",
)

## Redirect the previous canonical URL, along with all children whose slug has not changed
perm(r"everyone-has-a-story(.*)", "/consumer-tools/everyone-has-a-story$1")

## Shorter URL for Debt Collection Stories
perm(
    r"debt-?collection-?stories",
    "/consumer-tools/everyone-has-a-story/debt-collection/",
)

# Short URL for use in the Spanish OA Lump Sum Payment Guide, requested February 2017
perm(
    r"es/guia-asesor-financiero",
    "https://pueblo.gpo.gov/CFPBPubs/CFPBPubs.php?PubID=13114",
)

# Redirects associated with moving Older Americans and MSEM to Wagtail
## This one specific page got moved to another specific page
perm(
    r"older-americans/protecting-whats-yours",
    "/consumer-tools/educator-tools/resources-for-older-adults/protecting-whats-yours/",
)

## Send everything else beginning with /older-americans to the new main Resources for Older Adults page
perm(
    r"older-americans/",
    "/consumer-tools/educator-tools/resources-for-older-adults/",
)

## MSEM moved under Resources for Older Adults
perm(
    r"managing-someone-elses-money",
    "/consumer-tools/managing-someone-elses-money/",
)

# Redirect old Tax Preparers URL to its new Wagtail home
perm(
    r"tax-preparer-resources",
    "/consumer-tools/educator-tools/resources-for-tax-preparers/",
)

# Redirect FY13-17 Strategic Plan page to PDF to move out of WordPress
# See discussion here: https://GHE/CFGOV/platform/issues/710
temp(
    r"strategic-plan/",
    "https://files.consumerfinance.gov/f/strategic-plan.pdf",
)

# Redirects associated with moving Library Resources to Wagtail
## Specific redirects for changed pages
perm(
    r"library-resources/marketing-materials",
    "/consumer-tools/educator-tools/library-resources/outreach-materials-to-use-in-the-library/",
)
perm(
    r"library-resources/websites-videos-courses",
    "/consumer-tools/educator-tools/library-resources/online-resources/",
)

## Redirect main sublanding page, Librarian Training, and Program Ideas, which all have the same slug
perm(
    r"library-resources(.*)",
    "/consumer-tools/educator-tools/library-resources$1",
)

## Sending-money moved under Consumer Tools, along with all children whose slug has not changed
perm(r"sending-money(.*)", "/consumer-tools/sending-money$1")

## Servicemembers redirects
perm(
    r"servicemembers/on-demand-forums-and-tools",
    "/consumer-tools/educator-tools/servicemembers/webinars/",
)
perm(
    r"servicemembers/(.*)",
    "/consumer-tools/educator-tools/servicemembers/$1",
)
perm(
    r"practitioner-resources/servicemembers/additionalresources",
    "/consumer-tools/military-financial-lifecycle/",
)
perm(
    r"practitioner-resources/servicemembers/planning",
    "/consumer-tools/military-financial-lifecycle/",
)
perm(
    r"practitioner-resources/servicemembers/planning/creativesavingsstrategies",
    "/consumer-tools/military-financial-lifecycle/",
)
perm(
    r"practitioner-resources/servicemembers/protecting",
    "/consumer-tools/military-financial-lifecycle/",
)

# Common misspellings
temp(r"(.*)morgage(.*)", "$1mortgage$2")

# Redirects, requested by Rachael Keeler in July 2019
# https://GHE/CFGOV/platform/issues/3484
perm(r"about-us/advisory-groups/(.*)", "/rules-policy/advisory-committees/$1")
perm(r"askcfpb/search/(.*)", "/ask-cfpb/search/$1")
perm(
    r"how-to-prepare-your-finances-for-buying-a-home/(.*)",
    "/owning-a-home/prepare/",
)
temp(r"owning-a-home/help-us-improve/", "/owning-a-home/feedback/")
perm(r"wp-content/uploads/(.*)", "https://files.consumerfinance.gov/f/$1")
