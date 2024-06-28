"use strict";

// Class definition
var DatatablesServerSide = function() {
    // Shared variables
    var table;
    var dt;
    // Private functions
    var initDatatable = function() {
        
        dt = $("#employee_management-datatable").DataTable({
            searchDelay: 500,
            serverSide: true,
            responsive: false,
            pageLength: 25,
            processing: true,
            order: [
                [0, 'desc']
            ],
            select: {
                style: 'multi',
                selector: 'td:first-child input[type="checkbox"]',
                className: 'row-selected'
            },
            ajax: {
                method: "POST",
                url: `${api_config.datatable}`,
                data: {
                    'csrfmiddlewaretoken': `${api_config.csrfmiddlewaretoken}`,
                },
            },
            columns: [
                {data: 'id'},              
                {data: 'name'},
                {data: 'email'},
                {data: 'phonenumber'},
                {data: 'created_date'},
                {data: 'is_active'},
                {data: 'id'},
                {data: 'id'},
            ],
            columnDefs: [
                {
                    targets: 0,
                    orderable: false,
                    render: function (data) {
                        return `
                            <div class="form-check form-check-sm form-check-custom form-check-solid">
                                <input class="form-check-input checkbox-input-id" type="checkbox" value="${data}" />
                            </div>`;
                    }
                },
                {
                    targets: 1,
                    orderable: false,
                },
                {
                    targets: 2,
                    orderable: false,
                },
                {
                    targets: 3,
                    orderable: false,
                },
                {
                    targets: 4,
                    orderable: false,
                },
                {
                    searchable: false,
                    orderable: false,
                    targets: 5,
                    render: function(data, type, row) {
                        let label_badge_change = '';
                        if(data == 'True'){
                            label_badge_change = `<span style="cursor:pointer" data-id=${row.id}  class="btn btn-sm btn-outline btn-outline-dashed btn-outline-success btn-active-light-success active_inactive_language">Active</span>`;
                        }else if(data == 'False'){
                            label_badge_change =  `<span style="cursor:pointer" data-id=${row.id}  class="btn btn-sm btn-outline btn-outline-dashed btn-outline-danger btn-active-light-danger active_inactive_language">Inactive</span>`;
                        }
                        return label_badge_change;
                    }
                },
                {
                    targets: -2,
                    data: null,
                    orderable: false,
                    className: 'text-end',
                    render: function (data, type, row) {
                        let settings_edit_url = api_config.settings_edit_url.replace('0', row.encrypt_id.toString());
                        return `
                                    <a href="${settings_edit_url}" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm">
                                        <span class="svg-icon svg-icon-3">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                                            <path d="M19.14 12.9362C19.14 12.6362 19.164 12.3362 19.164 12.0362C19.164 11.7362 19.14 11.4362 19.14 11.1362L21.34 9.39621C21.54 9.24621 21.564 8.94621 21.4 8.73621L19.2 6.09621C19.06 5.89621 18.78 5.84621 18.6 5.99621L16.38 7.17621C15.9 6.81621 15.36 6.54621 14.8 6.39621L14.4 3.99621C14.36 3.77621 14.14 3.63621 13.92 3.63621H10.08C9.86 3.63621 9.64 3.77621 9.6 3.99621L9.2 6.39621C8.64 6.54621 8.1 6.81621 7.62 7.17621L5.4 5.99621C5.22 5.84621 4.94 5.89621 4.8 6.09621L2.6 8.73621C2.44 8.94621 2.46 9.24621 2.66 9.39621L4.86 11.1362C4.86 11.4362 4.84 11.7362 4.84 12.0362C4.84 12.3362 4.86 12.6362 4.86 12.9362L2.66 14.6762C2.46 14.8262 2.44 15.1262 2.6 15.3362L4.8 17.9762C4.94 18.1762 5.22 18.2262 5.4 18.0762L7.62 16.8962C8.1 17.2562 8.64 17.5262 9.2 17.6762L9.6 20.0762C9.64 20.2962 9.86 20.4362 10.08 20.4362H13.92C14.14 20.4362 14.36 20.2962 14.4 20.0762L14.8 17.6762C15.36 17.5262 15.9 17.2562 16.38 16.8962L18.6 18.0762C18.78 18.2262 19.06 18.1762 19.2 17.9762L21.4 15.3362C21.564 15.1262 21.54 14.8262 21.34 14.6762L19.14 12.9362ZM12 15.6362C10.54 15.6362 9.36 14.4562 9.36 12.9962C9.36 11.5362 10.54 10.3562 12 10.3562C13.46 10.3562 14.64 11.5362 14.64 12.9962C14.64 14.4562 13.46 15.6362 12 15.6362Z" fill="currentColor"/>
                                        </svg>

                                        </span>
                                    </a>
                                </div>
                        `;
                    },
                },
                {
                    targets: -1,
                    data: null,
                    orderable: false,
                    className: 'text-end',
                    render: function (data, type, row) {
                        let edit_url = api_config.edit_url.replace('0', row.encrypt_id.toString());
                        return `
                                <div class="d-flex justify-content-end flex-shrink-0">
                                    <a href="${edit_url}" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1">
                                        <span class="svg-icon svg-icon-3">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                                                <path opacity="0.3" d="M21.4 8.35303L19.241 10.511L13.485 4.755L15.643 2.59595C16.0248 2.21423 16.5426 1.99988 17.0825 1.99988C17.6224 1.99988 18.1402 2.21423 18.522 2.59595L21.4 5.474C21.7817 5.85581 21.9962 6.37355 21.9962 6.91345C21.9962 7.45335 21.7817 7.97122 21.4 8.35303ZM3.68699 21.932L9.88699 19.865L4.13099 14.109L2.06399 20.309C1.98815 20.5354 1.97703 20.7787 2.03189 21.0111C2.08674 21.2436 2.2054 21.4561 2.37449 21.6248C2.54359 21.7934 2.75641 21.9115 2.989 21.9658C3.22158 22.0201 3.4647 22.0084 3.69099 21.932H3.68699Z" fill="currentColor" />
                                                <path d="M5.574 21.3L3.692 21.928C3.46591 22.0032 3.22334 22.0141 2.99144 21.9594C2.75954 21.9046 2.54744 21.7864 2.3789 21.6179C2.21036 21.4495 2.09202 21.2375 2.03711 21.0056C1.9822 20.7737 1.99289 20.5312 2.06799 20.3051L2.696 18.422L5.574 21.3ZM4.13499 14.105L9.891 19.861L19.245 10.507L13.489 4.75098L4.13499 14.105Z" fill="currentColor" />
                                            </svg>
                                        </span>
                                    </a>
                                    <a href="javascript:void(0)" data-id=${row.id} data-admins-table-filter="delete_row" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm">
                                        <span class="svg-icon svg-icon-3">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                                                <path d="M5 9C5 8.44772 5.44772 8 6 8H18C18.5523 8 19 8.44772 19 9V18C19 19.6569 17.6569 21 16 21H8C6.34315 21 5 19.6569 5 18V9Z" fill="currentColor" />
                                                <path opacity="0.5" d="M5 5C5 4.44772 5.44772 4 6 4H18C18.5523 4 19 4.44772 19 5V5C19 5.55228 18.5523 6 18 6H6C5.44772 6 5 5.55228 5 5V5Z" fill="currentColor" />
                                                <path opacity="0.5" d="M9 4C9 3.44772 9.44772 3 10 3H14C14.5523 3 15 3.44772 15 4V4H9V4Z" fill="currentColor" />
                                            </svg>
                                        </span>
                                    </a>
                                </div>
                        `;
                    },
                },
                
                
            ],
            // Add data-filter attribute
            drawCallback: function(settings) {},
            createdRow: function(row, data, dataIndex) {
                $(row).find('td:eq(4)').attr('data-filter', data.CreditCardType);
            }
        });

        table = dt.$;
        // Re-init functions on every table re-draw -- more info: https://datatables.net/reference/event/draw
        dt.on('draw', function() {
            initToggleToolbar();
            toggleToolbars();
            handleDeleteRows();
            handleStatusFilter();
            ActiveOrIncativeUser();
            KTMenu.createInstances();
        });
    }

    // Search Datatable --- official docs reference: https://datatables.net/reference/api/search()
    var handleSearchDatatable = function() {
        const filterSearch = document.querySelector('[data-admins-table-filter="search"]');
        filterSearch.addEventListener('keyup', function(e) {
            dt.search(e.target.value).draw();
        });
    }

    // Handle status filter dropdown
    var handleStatusFilter = () => {
        const filterStatus = document.querySelector('[data-admins-filter="status"]');
        $(filterStatus).on('change', e => {
            let value = e.target.value;
            if(value === 'all'){
                value = '';
            }
            dt.column(3).search(value).draw();
        });
    }

    


    // Delete customer
    var handleDeleteRows = () => {
        // Select all delete buttons
        const deleteButtons = document.querySelectorAll('[data-admins-table-filter="delete_row"]');

        deleteButtons.forEach(d => {
            // Delete button on click
            d.addEventListener('click', function(e) {

                const destroyRecordIds = [$(this).data('id')];
                e.preventDefault();
                // Select parent row
                const parent = e.target.closest('tr');
                // Get customer name
                const userName = parent.querySelectorAll('td')[1].innerText;

                //     // SweetAlert2 pop up --- official docs reference: https://sweetalert2.github.io/
                Swal.fire({
                    text: "Are you sure you want to delete?",
                    icon: "warning",
                    showCancelButton: true,
                    buttonsStyling: false,
                    confirmButtonText: "Yes, delete!",
                    cancelButtonText: "No, cancel",
                    customClass: {
                        confirmButton: "btn fw-bold btn-danger",
                        cancelButton: "btn fw-bold btn-active-light-primary"
                    }
                }).then(function(result) {
                    if (result.value) {
                        $.post(`${api_config.delete_records}`, { ids: destroyRecordIds }, function(data, status, xhr) {

                            if (data.status_code == 200) {
                                Swal.fire({
                                    text: "Deleted Successfully",
                                    icon: "success",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn fw-bold btn-primary",
                                    }
                                }).then(function() {
                                    // delete row data from server and re-draw datatable
                                    dt.draw();
                                });

                            } else {
                                Swal.fire({
                                    text: "Something went wrong.",
                                    icon: "error",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn fw-bold btn-primary",
                                    }
                                });
                            }

                        }, 'json').done(function() {
                            console.log('Request done!');
                        }).fail(function(jqxhr, settings, ex) {
                            console.log('failed, ' + ex);
                            Swal.fire({
                                text: "Something went wrong.",
                                icon: "error",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn fw-bold btn-primary",
                                }
                            });
                        });

                    } else if (result.dismiss === 'cancel') {
                        Swal.fire({
                            text: userName + " was not deleted.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn fw-bold btn-primary",
                            }
                        });
                    }
                });
            })
        });
    }
    var ActiveOrIncativeUser = ()=>{
        const activeButton = document.getElementsByClassName('active_inactive_language')
        activeButton.forEach(d => {
            d.addEventListener('click', function(e) {
                const activeId = $(this).data('id');
                e.preventDefault();
                Swal.fire({
                    text: "Are you sure you want to change status",
                    icon: "warning",
                    showCancelButton: true,
                    buttonsStyling: true,
                    confirmButtonText: "Yes",
                    cancelButtonText: "No, return",
                    customClass: {
                        confirmButton: "btn btn-primary",
                        cancelButton: "btn btn-active-light"
                    }
                }).then(function(result){
                    if(result.value){               
                        $.post(`${api_config.active_inactive_company}`, {id:activeId }, function(data, status, xhr) {
                            if (data.status_code == 200) {
                                Swal.fire({
                                    text: "Successfully changed status ",
                                    icon: "success",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn btn-primary"
                                    }
                                }).then(function() {
                                    dt.draw();
                                });
    
                            } else {
                                Swal.fire({
                                    text: "Something went wrong.",
                                    icon: "error",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn fw-bold btn-primary",
                                    }
                                });
                            }
                        })
                    }
                })
            });
        });
    }

    // Init toggle toolbar
    var initToggleToolbar = function() {
        // Toggle selected action toolbar
        // Select all checkboxes
        const container = document.querySelector('#employee_management-datatable');
        const checkboxes = container.querySelectorAll('[type="checkbox"]');

        // Select elements
        const deleteSelected = document.querySelector('[data-admins-table-select="delete_selected"]');

        // Toggle delete selected toolbar
        checkboxes.forEach(c => {
            // Checkbox on click event
            c.addEventListener('click', function() {
                setTimeout(function() {
                    toggleToolbars();
                }, 50);
            });
        });

        // Deleted selected rows
        deleteSelected.addEventListener('click', function() {

            const row_ids = []
            $(".checkbox-input-id:checkbox:checked").each(function() {
                row_ids.push($(this).val());
            });

            Swal.fire({
                text: "Are you sure you want to delete selected admins?",
                icon: "warning",
                showCancelButton: true,
                buttonsStyling: false,
                showLoaderOnConfirm: true,
                confirmButtonText: "Yes, delete!",
                cancelButtonText: "No, cancel",
                customClass: {
                    confirmButton: "btn fw-bold btn-danger",
                    cancelButton: "btn fw-bold btn-active-light-primary"
                },
            }).then(function(result) {
                if (result.value) {

                    $.post(`${api_config.delete_records}`, { ids: row_ids }, function(data, status, xhr) {

                        if (data.status = 200) {
                            Swal.fire({
                                text: "You have deleted all selected admins!.",
                                icon: "success",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn fw-bold btn-primary",
                                }
                            }).then(function() {
                                // delete row data from server and re-draw datatable
                                dt.draw();
                                const headerCheckbox = container.querySelectorAll('[type="checkbox"]')[0];
                                headerCheckbox.checked = false;
                            });

                        } else {
                            Swal.fire({
                                text: "Something went wrong.",
                                icon: "error",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn fw-bold btn-primary",
                                }
                            });
                        }

                    }, 'json').done(function() {
                        console.log('Request done!');
                    }).fail(function(jqxhr, settings, ex) {
                        console.log('failed, ' + ex);
                        Swal.fire({
                            text: "Something went wrong.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn fw-bold btn-primary",
                            }
                        });
                    });

                } else if (result.dismiss === 'cancel') {
                    Swal.fire({
                        text: "Selected category was not deleted.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn fw-bold btn-primary",
                        }
                    });
                }
            });
        });
    }

    // Toggle toolbars
    var toggleToolbars = function() {
        // Define variables
        const container = document.querySelector('#employee_management-datatable');
        const toolbarBase = document.querySelector('[data-table-toolbar="base"]');
        const toolbarSelected = document.querySelector('[data-admins-table-toolbar="selected"]');
        const selectedCount = document.querySelector('[data-admins-table-select="selected_count"]');

        // Select refreshed checkbox DOM elements
        const allCheckboxes = container.querySelectorAll('tbody [type="checkbox"]');

        // Detect checkboxes state & count
        let checkedState = false;
        let count = 0;

        // Count checked boxes
        allCheckboxes.forEach(c => {
            if (c.checked) {
                checkedState = true;
                count++;
            }
        });

        // Toggle toolbars
        if (checkedState) {
            selectedCount.innerHTML = count;
            toolbarBase.classList.add('d-none');
            toolbarSelected.classList.remove('d-none');
        } else {
            toolbarBase.classList.remove('d-none');
            toolbarSelected.classList.add('d-none');
        }
    }

    // Public methods
    return {
        init: function() {
            initDatatable();
            handleSearchDatatable();
            initToggleToolbar();
            handleDeleteRows();
            handleStatusFilter ();
            ActiveOrIncativeUser();

        }
    }
}();

// On document ready
KTUtil.onDOMContentLoaded(function() {
    DatatablesServerSide.init();
});