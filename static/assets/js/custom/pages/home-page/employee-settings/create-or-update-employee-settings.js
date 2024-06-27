"use strict";

// Class definition
var MCUpdateOrCreateAdmin = function () {
    
    const handleSubmit = () => {
        let validator;
        

        // Get elements
        const form = document.getElementById('create-or-update-admin-form');
        const submitButton = document.getElementById('create-or-update-admin-submit');


        // var isImageEdit = document.getElementById('add-image-view').dataset.imageEdit === 'true';
        var isImageEdit = document.getElementById('casestudy_id').value;
        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    'name': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'email': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            emailAddress: {
                                message: 'The value is not a valid email address'
                            }
                        }
                    }, 
                    'phonenumber': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                        }
                    },
                    
                    
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: '.fv-row',
                        eleInvalidClass: '',
                        eleValidClass: ''
                    })
                },
                
            }
        );
        
        submitButton.addEventListener('click', e => {
            e.preventDefault();
            // Validate form before submit
            if (validator) {
                validator.validate().then(function (status) {
                    
                    console.log('validated!');
                    submitButton.setAttribute('data-kt-indicator', 'on');

                    // Disable button to avoid multiple click
                    submitButton.disabled = true;

                    if (status == 'Valid') {
                        const repeaterData = [];
                        debugger;
                        document.querySelectorAll('[data-repeater-item]').forEach(item => {
                            const name = item.querySelector('input[type="text"]').value;
                            const type = item.querySelector('select').value;
                            const value = item.querySelectorAll('input[type="text"]')[1].value;
                            repeaterData.push({ name, type, value });
                        });

                        // Stringify the data
                        const repeaterDataString = JSON.stringify(repeaterData);

                        // Append the stringified data to the form
                        const repeaterDataInput = document.createElement('input');
                        repeaterDataInput.type = 'hidden';
                        repeaterDataInput.name = 'repeater_data';
                        repeaterDataInput.value = repeaterDataString;
                        form.appendChild(repeaterDataInput);

                        // Handle submit button
                        e.preventDefault();
                        const btn = document.getElementById('create-or-update-admin-submit');
                        const text = document.getElementById('banner-loader-text');
                        btn.disabled = true;
                        btn.style.display = 'none';
                        text.style.display = 'block';
                        submitButton.setAttribute('data-kt-indicator', 'on');

                        // Disable submit button whilst loading
                        submitButton.disabled = true;
                        submitButton.removeAttribute('data-kt-indicator');
                        // Enable submit button after loading
                        submitButton.disabled = false;

                        // Redirect to customers list page
                        form.submit();
                    } else {
                        submitButton.removeAttribute('data-kt-indicator');

                        // Enable button
                        submitButton.disabled = false;
                        Swal.fire({
                            html: "Sorry, looks like there are some errors detected, please try again.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        });
                    }
                });
            }
        });
    }

    
    // Public methods
    return {
        init: function () {
            handleSubmit();
        }
    };
}();




// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateAdmin.init();
});