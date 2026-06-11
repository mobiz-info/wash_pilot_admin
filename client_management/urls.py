from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('client/', views.client_list, name='client_list'),
    path('client/create/', views.client_create, name='client_create'),
    path('client/edit/<uuid:id>/', views.client_edit, name='client_edit'),
    path('client/delete/<uuid:id>/', views.client_delete, name='client_delete'),
    path('ajax/states/', views.ajax_get_states, name='ajax_get_states'),
    path('ajax/areas/', views.ajax_get_areas, name='ajax_get_areas'),
    path('ajax/district/', views.ajax_get_districts, name='ajax_get_districts'),
    
    # Subscription
    path('subscription/', views.subscription_list, name='subscription_list'),
    path('subscription/create/', views.subscription_create, name='subscription_create'),
    path('subscription/edit/<uuid:id>/', views.subscription_edit, name='subscription_edit'),
    path('subscription/delete/<uuid:id>/', views.subscription_delete, name='subscription_delete'),

    # Branch Management
    path('branch/', views.branch_list, name='branch_list'),
    path('branch/create/', views.branch_create, name='branch_create'),
    path('branch/edit/<uuid:id>/', views.branch_edit, name='branch_edit'),
    path('branch/delete/<uuid:id>/', views.branch_delete, name='branch_delete'),

    # Staff Management
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/create/', views.staff_create, name='staff_create'),
    path('staff/edit/<uuid:id>/', views.staff_edit, name='staff_edit'),
    path('staff/delete/<uuid:id>/', views.staff_delete, name='staff_delete'),
    path('staff/salary/', views.staff_salary_list, name='staff_salary_list'),
    path('staff/salary/edit/<uuid:id>/', views.staff_salary_edit, name='staff_salary_edit'),

    # Staff Leaves
    path('staff/leaves/', views.staff_leave_list, name='staff_leave_list'),
    path('staff/leaves/create/', views.staff_leave_create, name='staff_leave_create'),
    path('staff/leaves/edit/<uuid:id>/', views.staff_leave_edit, name='staff_leave_edit'),
    path('staff/leaves/delete/<uuid:id>/', views.staff_leave_delete, name='staff_leave_delete'),

    # Stock Management
    path('stock/', views.stock_list, name='stock_list'),
    path('stock/create/', views.stock_create, name='stock_create'),
    path('stock/edit/<uuid:id>/', views.stock_edit, name='stock_edit'),
    path('stock/delete/<uuid:id>/', views.stock_delete, name='stock_delete'),

    # Customer Type
    path('customer-type/', views.customer_type_list, name='customer_type_list'),
    path('customer-type/create/', views.customer_type_create, name='customer_type_create'),
    path('customer-type/edit/<uuid:id>/', views.customer_type_edit, name='customer_type_edit'),
    path('customer-type/delete/<uuid:id>/', views.customer_type_delete, name='customer_type_delete'),

    # Customer Management
    path('customer/', views.customer_list, name='customer_list'),
    path('customer/create/', views.customer_create, name='customer_create'),
    path('customer/edit/<uuid:id>/', views.customer_edit, name='customer_edit'),
    path('customer/delete/<uuid:id>/', views.customer_delete, name='customer_delete'),
    path('ajax/load-vehicle-models/', views.ajax_load_vehicle_models, name='ajax_load_vehicle_models'),

    # Scheme Management
    path('scheme/', views.scheme_list, name='scheme_list'),
    path('scheme/usages/', views.scheme_usage_list, name='scheme_usage_list'),
    path('scheme/create/', views.scheme_create, name='scheme_create'),
    path('scheme/edit/<uuid:id>/', views.scheme_edit, name='scheme_edit'),
    path('scheme/delete/<uuid:id>/', views.scheme_delete, name='scheme_delete'),
    path('scheme/detail/<uuid:id>/', views.scheme_detail, name='scheme_detail'),
    path('scheme/<uuid:scheme_id>/voucher/add/', views.voucher_add, name='voucher_add'),
    path('voucher/delete/<uuid:voucher_id>/', views.voucher_delete, name='voucher_delete'),

    # Vehicle Management
    path('customer-vehicle/', views.customer_vehicle_list, name='customer_vehicle_list'),
    path('customer-vehicle/create/', views.customer_vehicle_create, name='customer_vehicle_create'),
    path('customer-vehicle/edit/<uuid:pk>/', views.customer_vehicle_edit, name='customer_vehicle_edit'),
    path('customer-vehicle/delete/<uuid:pk>/', views.customer_vehicle_delete, name='customer_vehicle_delete'),

    # Mobile API Endpoints
    path('api/login/', api_views.api_login, name='api_login'),
    path('api/customer/search/', api_views.api_customer_search, name='api_customer_search'),
    path('api/invoice/services/', api_views.api_get_services, name='api_get_services'),
    path('api/invoice/create/', api_views.api_create_invoice, name='api_create_invoice'),
    path('api/customer/form-data/', api_views.api_get_form_data, name='api_get_form_data'),
    
    # Expense APIs
    path('api/expenses/heads/', api_views.api_get_expense_heads, name='api_get_expense_heads'),
    path('api/expenses/create/', api_views.api_create_expense_entry, name='api_create_expense_entry'),
    
    # Staff Leaves APIs
    path('api/staff/list/', api_views.api_get_staff_list, name='api_get_staff_list'),
    path('api/staff/leaves/', api_views.api_get_staff_leaves, name='api_get_staff_leaves'),
    path('api/staff/leaves/create/', api_views.api_create_staff_leave, name='api_create_staff_leave'),

    path('api/customer/add/', api_views.api_add_customer, name='api_add_customer'),
    path('api/customer/list/', api_views.api_list_customers, name='api_list_customers'),
    path('api/customer/get/', api_views.api_get_customer, name='api_get_customer'),
    path('api/customer/edit/', api_views.api_edit_customer, name='api_edit_customer'),
    path('api/vehicle/search/', api_views.api_vehicle_search, name='api_vehicle_search'),
    path('api/dashboard/stats/', api_views.api_dashboard_stats, name='api_dashboard_stats'),
    path('api/company/branches/', api_views.api_company_branches, name='api_company_branches'),
    path('api/schemes/available/', api_views.api_available_schemes, name='api_available_schemes'),
    path('api/schemes/branch/', api_views.api_branch_schemes, name='api_branch_schemes'),
    path('api/schemes/options/', api_views.api_scheme_options, name='api_scheme_options'),
    path('api/schemes/create/', api_views.api_create_scheme, name='api_create_scheme'),
    path('api/schemes/validate-voucher/', api_views.api_validate_voucher, name='api_validate_voucher'),

    # Reports
    path('api/reports/jobs/', api_views.api_report_jobs, name='api_report_jobs'),
    path('api/reports/scheme-beneficiary/', api_views.api_report_scheme_beneficiary, name='api_report_scheme_beneficiary'),
    path('api/reports/collection/', api_views.api_report_collection, name='api_report_collection'),
    path('api/reports/outstanding/', api_views.api_report_outstanding, name='api_report_outstanding'),
    path('api/reports/bookings/', api_views.api_report_bookings, name='api_report_bookings'),
    path('api/reports/cancellations/', api_views.api_report_cancellations, name='api_report_cancellations'),
    path('api/reports/service-type/', api_views.api_report_service_type, name='api_report_service_type'),
    path('api/reports/service-type/detail/', api_views.api_report_service_type_detail, name='api_report_service_type_detail'),
    path('api/reports/service-type/vehicle-breakdown/', api_views.api_report_service_type_vehicle_breakdown, name='api_report_service_type_vehicle_breakdown'),
    path('api/reports/profit-loss/', api_views.api_report_profit_loss, name='api_report_profit_loss'),


    # Complaint Management
    path('api/complaint-types/', api_views.api_list_complaint_types, name='api_list_complaint_types'),
    path('api/complaint-types/create/', api_views.api_create_complaint_type, name='api_create_complaint_type'),
    path('api/complaints/create/', api_views.api_create_complaint, name='api_create_complaint'),
    path('api/complaints/list/', api_views.api_list_complaints, name='api_list_complaints'),
    path('api/complaints/update-status/', api_views.api_update_complaint_status, name='api_update_complaint_status'),

    # Complaint Web views
    path('complaint/', views.complaint_list, name='complaint_list'),
    path('complaint/create/', views.complaint_create, name='complaint_create'),
    path('complaint/resolve/<uuid:id>/', views.complaint_resolve, name='complaint_resolve'),
    path('complaint/type/create/', views.complaint_type_create, name='complaint_type_create'),

    # Company Web Settings (WhatsApp & Template)
    path('settings/whatsapp/', views.whatsapp_settings, name='whatsapp_settings'),
    path('settings/templates/', views.whatsapp_template_list, name='whatsapp_template_list'),
    path('settings/templates/create/', views.whatsapp_template_create, name='whatsapp_template_create'),
    path('settings/templates/edit/<uuid:id>/', views.whatsapp_template_edit, name='whatsapp_template_edit'),
    path('settings/templates/delete/<uuid:id>/', views.whatsapp_template_delete, name='whatsapp_template_delete'),
    
    path('customer-ledger/',views.customer_ledger,name='customer_ledger'),
    path('inactive-customer/',views.inactive_customer,name='inactive_customer'),
    path('new-customer/',views.new_customer,name='new_customer'),
    
    # Purchase Requests
    path('purchase-requests/', views.purchase_request_list, name='purchase_request_list'),
    path('purchase-requests/create/', views.purchase_request_create, name='purchase_request_create'),
    path('purchase-requests/edit/<uuid:id>/', views.purchase_request_edit, name='purchase_request_edit'),
    path('purchase-requests/delete/<uuid:id>/', views.purchase_request_delete, name='purchase_request_delete'),
    path('purchase-requests/approve/<uuid:id>/', views.purchase_request_approve, name='purchase_request_approve'),
    path('purchase-requests/reject/<uuid:id>/', views.purchase_request_reject, name='purchase_request_reject'),
    
    path('api/stock/list/', api_views.api_get_stock_list, name='api_get_stock_list'),
    path('api/purchase-requests/list/', api_views.api_get_purchase_requests, name='api_get_purchase_requests'),
    path('api/purchase-requests/create/', api_views.api_create_purchase_request, name='api_create_purchase_request'),
    path('api/expenses/heads/create/', api_views.api_create_expense_head, name='api_create_expense_head'),
    path('api/stock/create/', api_views.api_create_stock, name='api_create_stock'),
    path('api/extras/list/', api_views.api_get_extras_list, name='api_get_extras_list'),
    path('api/extras/create/', api_views.api_create_extra, name='api_create_extra'),
    path('api/reports/expense-head-wise/', api_views.api_report_expense_head_wise, name='api_report_expense_head_wise'),
    path('api/reports/expense-head-wise/detail/', api_views.api_report_expense_head_detail, name='api_report_expense_head_detail'),
    path('api/reports/leave/', api_views.api_report_leave, name='api_report_leave'),
]
