$(document).ready(function() {
    var pageTitle = "Prueba Técnica"; 
    
    $(window).blur(function() {
       document.title =  "Kenny Muñoz"; 
    });
    
    $(window).focus(function() {
      document.title = "Prueba Técnica";
    });

    var ky1_over = $('#ky1-ovr');
    var add_form = $('#add-frm');
    var trs_form = $('#add-trs');
    var cfm_msg = $('#cfm-msg');
    var frm_mess = $('#ky1-frm-msj');
    var trs_mess = $('#ky1-trs-msj');
    var edt_mess = $('#ky1-edt-msj');
    var usr_form = $('#usr-frm-edt');
    var frm = $('#ky1-add-user');
    var trs = $('#ky1-new-trs');

    $('#ky1-add-trs').on('click', function() {
        ky1_over.fadeToggle();
        trs_form.fadeToggle();
        $('#ky1-act').focus();
    });

    $('#trs-cls').on('click', function() {
        ky1_over.fadeToggle();
        trs_form.fadeToggle();
        trs_mess.stop(true, true).slideUp();
        trs[0].reset();
    });

    $('#trs-nop').on('click', function() {
        ky1_over.fadeToggle();
        trs_form.fadeToggle();
        trs_mess.stop(true, true).slideUp();
        trs[0].reset();
    });

    $('#trs-yes').on('click', function(e) {
        e.preventDefault();
        
        trs_mess.stop(true, true).slideUp('fast', function(){
            $.ajax({
                method: 'POST',
                url: '/trans',
                data: trs.serialize(),
                success: function(response) {
                    if (response.message === "OK") {
                        window.location.href = '/';
                    } else {
                        trs_mess.text(response.message).slideDown();
                    }
                },
                error: function(xhr, status, error) {
                    console.error(xhr.responseText);
                    console.error("Status: " + status);
                    console.error("Error: " + error);
                }
            });
        });
        
    });

    $('#ky1-add').on('click', function() {
        ky1_over.fadeToggle();
        add_form.fadeToggle();
        $('#ky1-dni').focus();
    });

    $('#frm-cls').on('click', function() {
        ky1_over.fadeToggle();
        add_form.fadeToggle();
        frm_mess.stop(true, true).slideUp();
        frm[0].reset();
    });

    $('#frm-nop').on('click', function() {
        ky1_over.fadeToggle();
        add_form.fadeToggle();
        frm_mess.stop(true, true).slideUp();
        frm[0].reset();
    });

    $('#frm-yes').on('click', function(e) {
        e.preventDefault();
        
        frm_mess.stop(true, true).slideUp('fast', function(){
            $.ajax({
                method: 'POST',
                url: '/create',
                data: frm.serialize(),
                success: function(response) {
                    if (response.message === "OK") {
                        window.location.href = '/';
                    } else {
                        frm_mess.text(response.message).slideDown();
                    }
                },
                error: function(xhr, status, error) {
                    console.error(xhr.responseText);
                    console.error("Status: " + status);
                    console.error("Error: " + error);
                }
            });
        });
        
    });

    $('#usr-del').on('click', function() {
        ky1_over.fadeToggle();
        cfm_msg.fadeToggle();
        
    });

    $('#msg-cls').on('click', function() {
        ky1_over.fadeToggle();
        cfm_msg.fadeToggle();
    });

    $('#msg-nop').on('click', function() {
        ky1_over.fadeToggle();
        cfm_msg.fadeToggle();
    });

    $('#usr-upd').on('click', function() {
        $('#usr-frm-edt').toggleClass('frm-edt');
        $('#usr-frm-edt input').prop('disabled', function(i, val) {
            return !val;
        });
        $('#btn-one').slideToggle();
        $('#btn-two').slideToggle();
    });

    $('#upd-nop').on('click', function() {
        $('#usr-frm-edt').toggleClass('frm-edt');
        $('#usr-frm-edt input').prop('disabled', function(i, val) {
            return !val;
        });
        $('#btn-one').slideToggle();
        $('#btn-two').slideToggle();
    });
    
    $('#upd-yes').on('click', function(e) {
        e.preventDefault();
        
        edt_mess.stop(true, true).slideUp('fast', function(){
            $.ajax({
                method: 'POST',
                url: '/update',
                data: usr_form.serialize(),
                success: function(response) {
                    if (response.message === "OK") {
                        window.location.href = '/';
                    } else {
                        edt_mess.text(response.message).slideDown();
                    }
                },
                error: function(xhr, status, error) {
                    console.error(xhr.responseText);
                    console.error("Status: " + status);
                    console.error("Error: " + error);
                }
            });
        });
        
    });    
    
    
  });