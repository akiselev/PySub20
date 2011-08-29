/* libsub.i */
 %module libsub
 %include "cstring.i"
 %{
    /* Put header files here or function declarations like below */
    /* extern int sub_errno;
    extern int sub_open( int dev );


    extern int sub_get_serial_number( int hndl, char *buf, int sz);
    extern int sub_get_product_id( int hndl, char *buf, int sz);
    extern int sub_close( int hndl );*/
    #include "libsub.h";
    
    #define PIN(x)  (1<<(x))

    int sub_gpio_read_pin(sub_handle dev, int pinnum)
    {
        int curr_pin_state;
        int status = sub_gpio_read(dev, &curr_pin_state);
        if (status) return -1;
        
        if (curr_pin_state & PIN(pinnum))
            return 1;
        else
            return 0;
    }
 %}
 
%cstring_output_maxsize(char *buf, int sz);
%cstring_chunk_output(sub_int32_t *get, 4);

%typemap(in) sub_device {
    $1 = PyInt_AsLong($input);
}

%typemap(out) sub_device {
    $result = PyInt_FromLong($1);
}

%typemap(in) sub_handle {
    $1 = PyInt_AsLong($input);
}

%typemap(out) sub_handle {
    $result = PyInt_FromLong($1);
}

%typemap(in) sub_int32_t {
    $1 = PyLong_AsLong($input);
}

%typemap(out) sub_int32_t {
    $result = PyLong_FromLong($1);
}

extern int sub_get_mode( sub_handle hndl, int *boot );

extern sub_device sub_find_devices( sub_device first );
extern sub_handle sub_open( sub_device dev );
extern int sub_close( sub_handle hndl );
extern const struct sub_version* sub_get_version( sub_handle hndl );
extern const struct sub_cfg_vpd* sub_get_cfg_vpd( sub_handle hndl );

/* GPIO */
extern int	sub_gpio_config( sub_handle hndl, sub_int32_t set, sub_int32_t* get, sub_int32_t mask );
extern int	sub_gpio_read( sub_handle hndl, sub_int32_t* get );
extern int	sub_gpio_write( sub_handle hndl, sub_int32_t set, sub_int32_t* get, sub_int32_t mask );
extern int  sub_gpio_read_pin(sub_handle dev, int pinnum);

/* Fast PWM */
extern int sub_fpwm_config( sub_handle hndl, double freq_hz, int flags );
extern int sub_fpwm_set( sub_handle hndl, int pwm_n, double duty );

/* LCD */
extern int	sub_lcd_write( sub_handle hndl, char* str );

/* product identification */
extern int sub_control_request( sub_handle hndl, int type, int request, int value, int index, char* buf, int sz, int timeout );
extern int sub_get_serial_number( sub_handle hndl, char *buf, int sz);
extern int sub_get_product_id( sub_handle hndl, char *buf, int sz);

extern char* sub_strerror( int errnum );
extern int	sub_get_errno( void ) ;
extern int sub_get_i2c_status( void ) ;
