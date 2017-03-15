$(document).ready(function () {
    // Generate a simple captcha
    function randomNumber(min, max) {
        return Math.floor(Math.random() * (max - min + 1) + min);
    };
    $('#captchaOperation').html([randomNumber(1, 20), '+', randomNumber(1, 30), '='].join(' '));

    $('#createSupplierForm').bootstrapValidator({
        fields: {
            name: {
                message: 'The supplier name is not valid',
                validators: {
                    notEmpty: {
                        message: 'The supplier name is required and can\'t be empty'
                    }
                }
            }
        }
    });

    $('#createManufacturerForm').bootstrapValidator({
        fields: {
            name: {
                message: 'The manufacturer name is not valid',
                validators: {
                    notEmpty: {
                        message: 'The manufacturer name is required and can\'t be empty'
                    }
                }
            }
        }
    });
    $('#createCompanyForm').bootstrapValidator({
        fields: {
            name: {
                message: 'The company name is not valid',
                validators: {
                    notEmpty: {
                        message: 'The company name is required and can\'t be empty'
                    }
                }
            }
        }
    });

    $('#createAssetForm').bootstrapValidator({
        fields: {
            model: {
                message: 'The model is not valid',
                validators: {
                    notEmpty: {
                        message: 'The model is required'
                    }
                }
            },
            status: {
                message: 'The status is not valid',
                validators: {
                    notEmpty: {
                        message: 'The status is required'
                    }
                }
            }
        }
    });

    $('#createLocationForm').bootstrapValidator({
        fields: {
            name: {
                message: 'The location name is not valid',
                validators: {
                    notEmpty: {
                        message: 'The location name is required and can\'t be empty'
                    }
                }
            }
        }
    });

    $('#createHardwareForm').bootstrapValidator({
        fields: {
            model: {
                message: 'The model name is not valid',
                validators: {
                    notEmpty: {
                        message: 'The model name is required and can\'t be empty'
                    }
                }
            },
            category: {
                message: 'The category is not valid',
                validators: {
                    notEmpty: {
                        message: 'The category is required'
                    }
                }
            },
            manufacturer: {
                message: 'The manufacturer is not valid',
                validators: {
                    notEmpty: {
                        message: 'The manufacturer is required'
                    }
                }
            }
        }
    });

    $('#createSoftwareForm').bootstrapValidator({
        fields: {
            name: {
                message: 'The software name is not valid',
                validators: {
                    notEmpty: {
                        message: 'The software name is required and can\'t be empty'
                    }
                }
            }

        }
    });
    $('#createUserForm').bootstrapValidator({
        fields: {
            fullname: {
                message: 'The fullname is not valid',
                validators: {
                    notEmpty: {
                        message: 'The fullname is required and can\'t be empty'
                    }
                }
            }
        }
    });

});