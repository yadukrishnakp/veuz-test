"use strict";

// Class definition
var MCUpdateOrCreateAdmin = function () {
    
    const handleSubmit = () => {
      
        let validator;
        

        // Get elements
        const form = document.getElementById('create-or-update-admin-form');
        const submitButton = document.getElementById('create-or-update-admin-submit');
        // var current_user   = document.getElementById('current_user_id').value;
       
        // if (!password_reset) {
        //     password_reset = 'none';
        // }
      

        // if (!current_user && !password_reset) {
        //     delete validatorsConfig.fields['password'].validators.notEmpty;
        // }
        submitButton.addEventListener('click', e => {
            e.preventDefault();
            var password_reset_btn = document.getElementById('password_hidden_id');
            var password_reset = password_reset_btn ? password_reset_btn.value : '';
            var casestudyId = document.getElementById('casestudy_id').value;
            let isPasswordValidate = false
            if(casestudyId==''){
                isPasswordValidate = true; 
            }else if(password_reset==''){
               isPasswordValidate = false
            }else if(password_reset){
                isPasswordValidate = true

            }
            validator = FormValidation.formValidation(
                form,
                {
                    fields: {
                        'full_name': {
                            validators: {
                                notEmpty: {
                                    message: 'This field is required'
                                }
                            }
                        },
                        'username': {
                            validators: {
                                notEmpty: {
                                    message: 'This field is required'
                                }
                            }
                        },
                        'password': {
                            validators: !isPasswordValidate ? {} : {
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
                        'mobile': {
                            validators: {
                                notEmpty: {
                                    message: 'This field is required'
                                },
                                numeric: {
                                    message: 'The value is not a number'
                                },
                                stringLength: {
                                    min: 10,
                                    max: 10,
                                    message: 'The phone number must be exactly 10 digits'
                                }
                            }
                        },
    
                        'groups': {
                            validators: {
                                notEmpty: {
                                    message: 'This field is required'
                                }
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
                    }
                }
            );
            
            
            const btn = document.getElementById('create-or-update-admin-submit');
            const text = document.getElementById('banner-loader-text');
           
            // Validate form before submit
            if (validator) {
                validator.validate().then(function (status) {
                    
                    // Disable button to avoid multiple click
                    if (status == 'Valid') {
                        submitButton.disabled = true;
                        btn.disabled = true;
                        btn.style.display = 'none';
                        text.style.display = 'block';
                        submitButton.setAttribute('data-kt-indicator', 'on');

                        // Handle submit button
                        // e.preventDefault();

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
                            html: "Please enter the required fields",
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