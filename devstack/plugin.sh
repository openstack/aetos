# Install and start **Aetos** service in devstack
#
# To enable Aetos in devstack add an entry to local.conf that
# looks like
#
# [[local|localrc]]
# enable_plugin aetos https://opendev.org/openstack/aetos

# Support potential entry-points console scripts in VENV or not
if [[ ${USE_VENV} = True ]]; then
    PROJECT_VENV["aetos"]=${AETOS_DIR}.venv
    AETOS_BIN_DIR=${PROJECT_VENV["aetos"]}/bin
else
    AETOS_BIN_DIR=$(get_python_exec_prefix)
fi

# Test if any Aetos services are enabled
# is_aetos_enabled
function is_aetos_enabled {
    [[ ,${ENABLED_SERVICES} =~ ,"aetos" ]] && return 0
    return 1
}

function aetos_service_url {
    echo "$AETOS_SERVICE_PROTOCOL://$AETOS_SERVICE_HOST/prometheus"
}

# Create aetos related accounts in Keystone
function _aetos_create_accounts {
    if is_service_enabled aetos; then

        create_service_user "aetos" "admin"

        get_or_create_service "aetos" "metric-storage" "OpenStack Aetos Service"
        get_or_create_endpoint 'metric-storage' "$REGION_NAME" "$(aetos_service_url)"
    fi
}

# cleanup_aetos() - Remove residual data files, anything left over
# from previous runs that a clean run would need to clean up
function cleanup_aetos {
    remove_uwsgi_config "$AETOS_UWSGI_CONF" "aetos"
}

# Configure Aetos
function configure_aetos {
    iniset $AETOS_CONF DEFAULT debug "$ENABLE_DEBUG_LOG_LEVEL"

    # Set up logging
    iniset $AETOS_CONF DEFAULT use_syslog $SYSLOG

    # Format logging
    setup_logging $AETOS_CONF DEFAULT

    configure_keystone_authtoken_middleware $AETOS_CONF aetos

    # iniset creates these files when it's called if they don't exist.
    write_uwsgi_config "$AETOS_UWSGI_CONF" "$AETOS_UWSGI" "/prometheus" "" "aetos"
}

# init_aetos() - Initialize etc.
function init_aetos {
    # Get aetos keystone settings in place
    _aetos_create_accounts
}

# Install Aetos.
function install_aetos {
    setup_develop $AETOS_DIR $AETOS_BACKEND
    sudo install -d -o $STACK_USER -m 755 $AETOS_CONF_DIR

    pip_install uwsgi
}

# start_aetos() - Start running processes, including screen
function start_aetos {
    run_process aetos "$AETOS_BIN_DIR/uwsgi --ini $AETOS_UWSGI_CONF"
}

# configure_tempest_for_aetos()
function configure_tempest_for_aetos {
    if is_service_enabled tempest; then
        iniset $TEMPEST_CONFIG service_available aetos True
    fi
}

# stop_aetos() - Stop running processes
function stop_aetos {
    stop_process aetos
}

# This is the main for plugin.sh
if is_service_enabled aetos; then
    if [[ "$1" == "stack" && "$2" == "install" ]]; then
        echo_summary "Installing Aetos"
        # Use stack_install_service here to account for virtualenv
        stack_install_service aetos
    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        echo_summary "Configuring Aetos"
        configure_aetos
    elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
        echo_summary "Initializing Aetos"
        # Tidy base for aetos
        init_aetos
        # Start the service
        start_aetos
    elif [[ "$1" == "stack" && "$2" == "test-config" ]]; then
        echo_summary "Configuring Tempest for Aetos"
        configure_tempest_for_aetos
    fi

    if [[ "$1" == "unstack" ]]; then
        echo_summary "Shutting Down Aetos"
        stop_aetos
    fi

    if [[ "$1" == "clean" ]]; then
        echo_summary "Cleaning Aetos"
        cleanup_aetos
    fi
fi
