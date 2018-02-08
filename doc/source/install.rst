.. contents:: Оглавление
    :depth: 3



Протокол восстановления (установки)
===================================

.. index:: install

Стандартный путь расположения приложения
----------------------------------------

**/srv/django/iss**

Структура каталогов проекта на 10.02.2017

 ::

        ├── iss
        │   ├── begin
        │   │   ├── admin.py
        │   │   ├── admin.pyc
        │   │   ├── apps.py
        │   │   ├── forms.py
        │   │   ├── forms.pyc
        │   │   ├── __init__.py
        │   │   ├── __init__.pyc
        │   │   ├── migrations
        │   │   │   ├── __init__.py
        │   │   │   └── __init__.pyc
        │   │   ├── models.py
        │   │   ├── models.pyc
        │   │   ├── tests.py
        │   │   ├── views.py
        │   │   └── views.pyc
        │   ├── context_processors.py
        │   ├── context_processors.pyc
        │   ├── dbconn.py
        │   ├── dbconn.pyc
        │   ├── equipment
        │   │   ├── admin.py
        │   │   ├── admin.pyc
        │   │   ├── apidata.py
        │   │   ├── apidata.pyc
        │   │   ├── apps.py
        │   │   ├── apps.pyc
        │   │   ├── __init__.py
        │   │   ├── __init__.pyc
        │   │   ├── jsondata.py
        │   │   ├── jsondata.pyc
        │   │   ├── management
        │   │   │   ├── commands
        │   │   │   │   ├── _add_devices2scan.py
        │   │   │   │   ├── device_list_catv.py
        │   │   │   │   ├── device_list_catv.pyc
        │   │   │   │   ├── device_list.py
        │   │   │   │   ├── device_list.pyc
        │   │   │   │   ├── device_tools.py
        │   │   │   │   ├── device_tools.pyc
        │   │   │   │   ├── device_tools_test.py
        │   │   │   │   ├── device_tools_test.pyc
        │   │   │   │   ├── get_issdata.py
        │   │   │   │   ├── get_issdata.pyc
        │   │   │   │   ├── get_issdata.py.orig
        │   │   │   │   ├── __init__.py
        │   │   │   │   ├── __init__.pyc
        │   │   │   │   ├── make_graph.py
        │   │   │   │   ├── make_graph.pyc
        │   │   │   │   ├── snmp_devices.py
        │   │   │   │   └── snmp_devices.pyc
        │   │   │   ├── __init__.py
        │   │   │   └── __init__.pyc
        │   │   ├── models.py
        │   │   ├── models.pyc
        │   │   ├── tests.py
        │   │   ├── urls.py
        │   │   ├── urls.pyc
        │   │   ├── views.py
        │   │   └── views.pyc
        │   ├── __init__.py
        │   ├── __init__.pyc
        │   ├── inventory
        │   │   ├── admin.py
        │   │   ├── admin.pyc
        │   │   ├── apps.py
        │   │   ├── __init__.py
        │   │   ├── __init__.pyc
        │   │   ├── jsondata.py
        │   │   ├── jsondata.pyc
        │   │   ├── models.py
        │   │   ├── models.pyc
        │   │   ├── tests.py
        │   │   ├── urls.py
        │   │   ├── urls.pyc
        │   │   ├── views.py
        │   │   └── views.pyc
        │   ├── localdicts
        │   │   ├── admin.py
        │   │   ├── admin.pyc
        │   │   ├── apps.py
        │   │   ├── apps.pyc
        │   │   ├── __init__.py
        │   │   ├── __init__.pyc
        │   │   ├── models.py
        │   │   ├── models.pyc
        │   │   ├── tests.py
        │   │   └── views.py
        │   ├── log
        │   ├── monitor
        │   │   ├── admin.py
        │   │   ├── admin.pyc
        │   │   ├── apps.py
        │   │   ├── filedata.py
        │   │   ├── filedata.pyc
        │   │   ├── __init__.py
        │   │   ├── __init__.pyc
        │   │   ├── jsondata.py
        │   │   ├── jsondata.pyc
        │   │   ├── management
        │   │   │   ├── commands
        │   │   │   │   ├── get_iss_drp.py
        │   │   │   │   ├── get_iss_drp.pyc
        │   │   │   │   ├── __init__.py
        │   │   │   │   ├── __init__.pyc
        │   │   │   │   ├── mail_sibttk_ru.py
        │   │   │   │   ├── mail_sibttk_ru.pyc
        │   │   │   │   ├── send_email_message.py
        │   │   │   │   ├── send_email_message.pyc
        │   │   │   │   ├── send_iss_accident.py
        │   │   │   │   ├── send_iss_accident.pyc
        │   │   │   │   ├── send_reports_accident.py
        │   │   │   │   ├── send_reports_accident.pyc
        │   │   │   │   ├── zenoss_krsk.py
        │   │   │   │   └── zenoss_krsk.pyc
        │   │   │   ├── __init__.py
        │   │   │   └── __init__.pyc
        │   │   ├── models.py
        │   │   ├── models.pyc
        │   │   ├── othersources.py
        │   │   ├── othersources.pyc
        │   │   ├── templatetags
        │   │   │   ├── __init__.py
        │   │   │   ├── __init__.pyc
        │   │   │   ├── monitor_extras.py
        │   │   │   └── monitor_extras.pyc
        │   │   ├── tests.py
        │   │   ├── tools.py
        │   │   ├── tools.pyc
        │   │   ├── urls.py
        │   │   ├── urls.pyc
        │   │   ├── views.py
        │   │   └── views.pyc
        │   ├── mydecorators.py
        │   ├── mydecorators.pyc
        │   ├── onyma
        │   │   ├── admin.py
        │   │   ├── admin.pyc
        │   │   ├── apidata.py
        │   │   ├── apidata.pyc
        │   │   ├── apps.py
        │   │   ├── __init__.py
        │   │   ├── __init__.pyc
        │   │   ├── models.py
        │   │   ├── models.pyc
        │   │   ├── soap
        │   │   │   ├── dognum_get_balans.php
        │   │   │   ├── ls_get_balans.php
        │   │   │   └── service.htms
        │   │   ├── tests.py
        │   │   ├── urls.py
        │   │   ├── urls.pyc
        │   │   └── views.py
        │   ├── settings.py
        │   ├── settings.pyc
        │   ├── urls.py
        │   ├── urls.pyc
        │   ├── working
        │   │   ├── admin.py
        │   │   ├── admin.pyc
        │   │   ├── apps.py
        │   │   ├── __init__.py
        │   │   ├── __init__.pyc
        │   │   ├── migrations
        │   │   │   ├── __init__.py
        │   │   │   └── __init__.pyc
        │   │   ├── models.py
        │   │   ├── models.pyc
        │   │   ├── tests.py
        │   │   ├── urls.py
        │   │   ├── urls.pyc
        │   │   ├── views.py
        │   │   └── views.pyc
        │   ├── wsgi.py
        │   └── wsgi.pyc
        ├── json_api.sh
        ├── manage.py
        ├── static
        │   ├── css
        │   │   ├── bootstrap.css
        │   │   ├── bootstrap.css.map
        │   │   ├── bootstrap-datetimepicker.css
        │   │   ├── bootstrap-datetimepicker.min.css
        │   │   ├── bootstrap.min.css
        │   │   ├── bootstrap.min.css.map
        │   │   ├── bootstrap-theme.css
        │   │   ├── bootstrap-theme.css.map
        │   │   ├── bootstrap-theme.min.css
        │   │   ├── bootstrap-theme.min.css.map
        │   │   ├── images
        │   │   │   ├── ui-icons_444444_256x240.png
        │   │   │   ├── ui-icons_555555_256x240.png
        │   │   │   ├── ui-icons_777620_256x240.png
        │   │   │   ├── ui-icons_777777_256x240.png
        │   │   │   ├── ui-icons_cc0000_256x240.png
        │   │   │   └── ui-icons_ffffff_256x240.png
        │   │   ├── jquery.multiselect.css
        │   │   ├── jquery-ui.css
        │   │   ├── jquery-ui.structure.css
        │   │   ├── jquery-ui.structure.min.css
        │   │   ├── jquery-ui.theme.css
        │   │   └── jquery-ui.theme.min.css
        │   ├── equipment
        │   │   ├── agregators.css
        │   │   ├── agregators.js
        │   │   ├── devices.css
        │   │   ├── devices.js
        │   │   ├── footnode.css
        │   │   ├── footnode.js
        │   │   ├── topology.css
        │   │   └── topology.js
        │   ├── favicon.ico
        │   ├── fonts
        │   │   ├── glyphicons-halflings-regular.eot
        │   │   ├── glyphicons-halflings-regular.svg
        │   │   ├── glyphicons-halflings-regular.ttf
        │   │   ├── glyphicons-halflings-regular.woff
        │   │   └── glyphicons-halflings-regular.woff2
        │   ├── inventory
        │   │   ├── devicescheme.css
        │   │   └── devicescheme.js
        │   ├── js
        │   │   ├── bootstrap-datetimepicker.min.js
        │   │   ├── bootstrap.js
        │   │   ├── bootstrap.min.js
        │   │   ├── datepicker-ru.js
        │   │   ├── jquery-2.2.4.js
        │   │   ├── jquery-3.1.0.min.js
        │   │   ├── jquery.json.js
        │   │   ├── jquery-migrate-1.4.1.min.js
        │   │   ├── jquery-migrate-3.0.0.js
        │   │   ├── jquery.multiselect.filter.js
        │   │   ├── jquery.multiselect.filter.ru.js
        │   │   ├── jquery.multiselect.js
        │   │   ├── jquery-ui.js
        │   │   ├── jquery-ui.min.js
        │   │   ├── jquery.validate.js
        │   │   ├── messages_ru.js
        │   │   └── npm.js
        │   ├── monitor
        │   │   ├── accidents.css
        │   │   ├── accidents.js
        │   │   ├── columns_filter.js
        │   │   ├── dialogs.js
        │   │   ├── dragtable.js
        │   │   ├── facefix.js
        │   │   ├── headfilter.js
        │   │   ├── jquery.tablescroll.js
        │   │   ├── messages.css
        │   │   ├── monitor.css
        │   │   ├── monitor.js
        │   │   └── user-settings.js
        │   └── working
        │       ├── working.css
        │       └── working.js
        ├── templates
        │   ├── begin.html
        │   ├── equipment
        │   │   ├── agregators_list.html
        │   │   ├── devices_list.html
        │   │   ├── footnode_list.html
        │   │   ├── form2.html
        │   │   ├── form3.html
        │   │   ├── form.html
        │   │   └── topology.html
        │   ├── footer.html
        │   ├── header.html
        │   ├── index.html
        │   ├── inventory
        │   │   ├── devicescheme_list.html
        │   │   └── schemeform.html
        │   ├── mainmenu.html
        │   ├── menu.html
        │   ├── monitor
        │   │   ├── accidentform2.html
        │   │   ├── accidentform.html
        │   │   ├── accident_list.html
        │   │   ├── containergroup.html
        │   │   ├── drplist.html
        │   │   ├── eventform.html
        │   │   ├── event_list.html
        │   │   ├── event_menu.html
        │   │   ├── mailform2.html
        │   │   ├── mailform.html
        │   │   ├── message_list.html
        │   │   ├── message_mss.html
        │   │   ├── tablehead.html
        │   │   ├── tablerowdata.html
        │   │   ├── usersettings.html
        │   │   └── zkllist.html
        │   └── working
        │       └── work_list.html
        ├── tools
        │   ├── backup
        │   │   ├── backup-db
        │   │   └── backup-dir
        │   └── zenapitool
        │       ├── config.py
        │       ├── config.pyc
        │       ├── device_list.txt
        │       ├── exception.py
        │       ├── exception.pyc
        │       ├── external.py
        │       ├── external.pyc
        │       ├── getdeviceip.sh
        │       ├── LICENSE
        │       ├── README.md
        │       ├── zenapitool.conf
        │       ├── zenapitool.log
        │       ├── zenapitool.py
        │       ├── zenoss.py
        │       └── zenoss.pyc



Версии установленого основного программного обеспечения
-------------------------------------------------------

python
~~~~~~

 ::

        >>> import platform
        >>> platform.python_version()
        '2.7.12'
        >>>


django
~~~~~~

 ::

    root@iss:/srv/django/iss# python manage.py shell
    Python 2.7.12 (default, Nov 19 2016, 06:48:10)
    Type "copyright", "credits" or "license" for more information.

    In [1]: import django

    In [2]: django.VERSION
    Out[2]: (1, 9, 6, 'final', 0)


postgresql
~~~~~~~~~~

 ::

    iss=# select version();
                                                      version
    -----------------------------------------------------------------------------------------------------------
     PostgreSQL 9.5.4 on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 6.1.1-11ubuntu12) 6.1.1 20160805, 64-bit
    (1 row)


postgresql.conf

 ::

    data_directory = '/var/lib/postgresql/9.5/main'		# use data in another directory
                        # (change requires restart)
    hba_file = '/etc/postgresql/9.5/main/pg_hba.conf'	# host-based authentication file
                        # (change requires restart)
    ident_file = '/etc/postgresql/9.5/main/pg_ident.conf'	# ident configuration file
                        # (change requires restart)

    # If external_pid_file is not explicitly set, no extra PID file is written.
    external_pid_file = '/var/run/postgresql/9.5-main.pid'			# write an extra PID file
                        # (change requires restart)


    #------------------------------------------------------------------------------
    # CONNECTIONS AND AUTHENTICATION
    #------------------------------------------------------------------------------

    # - Connection Settings -

    listen_addresses = '*'		# what IP address(es) to listen on;
                        # comma-separated list of addresses;
                        # defaults to 'localhost'; use '*' for all
                        # (change requires restart)
    port = 5432				# (change requires restart)
    max_connections = 200			# (change requires restart)
    # Note:  Increasing max_connections costs ~400 bytes of shared memory per
    # connection slot, plus lock space (see max_locks_per_transaction).
    #superuser_reserved_connections = 3	# (change requires restart)
    unix_socket_directories = '/var/run/postgresql'	# comma-separated list of directories
                        # (change requires restart)
    #unix_socket_group = ''			# (change requires restart)
    #unix_socket_permissions = 0777		# begin with 0 to use octal notation
                        # (change requires restart)
    #bonjour = off				# advertise server via Bonjour
                        # (change requires restart)
    #bonjour_name = ''			# defaults to the computer name
                        # (change requires restart)

    # - Security and Authentication -

    #authentication_timeout = 1min		# 1s-600s
    ssl = true				# (change requires restart)
    #ssl_ciphers = 'HIGH:MEDIUM:+3DES:!aNULL' # allowed SSL ciphers
                        # (change requires restart)
    #ssl_prefer_server_ciphers = on		# (change requires restart)
    #ssl_ecdh_curve = 'prime256v1'		# (change requires restart)
    ssl_cert_file = '/etc/ssl/certs/ssl-cert-snakeoil.pem'		# (change requires restart)
    ssl_key_file = '/etc/ssl/private/ssl-cert-snakeoil.key'		# (change requires restart)
    #ssl_ca_file = ''			# (change requires restart)
    #ssl_crl_file = ''			# (change requires restart)
    #password_encryption = on
    #db_user_namespace = off
    #row_security = on

    # GSSAPI using Kerberos
    #krb_server_keyfile = ''
    #krb_caseins_users = off

    # - TCP Keepalives -
    # see "man 7 tcp" for details

    #tcp_keepalives_idle = 0		# TCP_KEEPIDLE, in seconds;
                        # 0 selects the system default
    #tcp_keepalives_interval = 0		# TCP_KEEPINTVL, in seconds;
                        # 0 selects the system default
    #tcp_keepalives_count = 0		# TCP_KEEPCNT;
                        # 0 selects the system default


    #------------------------------------------------------------------------------
    # RESOURCE USAGE (except WAL)
    #------------------------------------------------------------------------------

    # - Memory -

    shared_buffers = 3072MB			# min 128kB
                        # (change requires restart)
    #huge_pages = try			# on, off, or try
                        # (change requires restart)
    temp_buffers = 32MB			# min 800kB
    #max_prepared_transactions = 0		# zero disables the feature
                        # (change requires restart)
    # Note:  Increasing max_prepared_transactions costs ~600 bytes of shared memory
    # per transaction slot, plus lock space (see max_locks_per_transaction).
    # It is not advisable to set max_prepared_transactions nonzero unless you
    # actively intend to use prepared transactions.
    work_mem = 128MB				# min 64kB
    maintenance_work_mem = 512MB		# min 1MB
    #autovacuum_work_mem = -1		# min 1MB, or -1 to use maintenance_work_mem
    #max_stack_depth = 2MB			# min 100kB
    dynamic_shared_memory_type = sysv	# the default is the first option
                        # supported by the operating system:
                        #   posix
                        #   sysv
                        #   windows
                        #   mmap
                        # use none to disable dynamic shared memory

    # - Disk -

    #temp_file_limit = -1			# limits per-session temp file space
                        # in kB, or -1 for no limit

    # - Kernel Resource Usage -

    #max_files_per_process = 1000		# min 25
                        # (change requires restart)
    #shared_preload_libraries = ''		# (change requires restart)

    # - Cost-Based Vacuum Delay -

    vacuum_cost_delay = 50			# 0-100 milliseconds
    vacuum_cost_page_hit = 6		# 0-10000 credits
    #vacuum_cost_page_miss = 10		# 0-10000 credits
    #vacuum_cost_page_dirty = 20		# 0-10000 credits
    vacuum_cost_limit = 100		# 1-10000 credits

    # - Background Writer -

    #bgwriter_delay = 200ms			# 10-10000ms between rounds
    #bgwriter_lru_maxpages = 100		# 0-1000 max buffers written/round
    #bgwriter_lru_multiplier = 2.0		# 0-10.0 multipler on buffers scanned/round

    # - Asynchronous Behavior -

    #effective_io_concurrency = 1		# 1-1000; 0 disables prefetching
    #max_worker_processes = 8


    #------------------------------------------------------------------------------
    # WRITE AHEAD LOG
    #------------------------------------------------------------------------------

    # - Settings -

    #wal_level = minimal			# minimal, archive, hot_standby, or logical
                        # (change requires restart)
    fsync = off				# turns forced synchronization on or off
    synchronous_commit = off		# synchronization level;
                        # off, local, remote_write, or on
    #wal_sync_method = fsync		# the default is the first option
                        # supported by the operating system:
                        #   open_datasync
                        #   fdatasync (default on Linux)
                        #   fsync
                        #   fsync_writethrough
                        #   open_sync
    full_page_writes = off			# recover from partial page writes
    #wal_compression = off			# enable compression of full-page writes
    #wal_log_hints = off			# also do full page writes of non-critical updates
                        # (change requires restart)
    wal_buffers = 256MB			# min 32kB, -1 sets based on shared_buffers
                        # (change requires restart)
    #wal_writer_delay = 200ms		# 1-10000 milliseconds

    #commit_delay = 0			# range 0-100000, in microseconds
    #commit_siblings = 5			# range 1-1000

    # - Checkpoints -

    checkpoint_timeout = 1h		# range 30s-1h
    max_wal_size = 2GB
    min_wal_size = 1GB
    checkpoint_completion_target = 0.7	# checkpoint target duration, 0.0 - 1.0
    #checkpoint_warning = 30s		# 0 disables

    # - Archiving -

    #archive_mode = off		# enables archiving; off, on, or always
                    # (change requires restart)
    #archive_command = ''		# command to use to archive a logfile segment
                    # placeholders: %p = path of file to archive
                    #               %f = file name only
                    # e.g. 'test ! -f /mnt/server/archivedir/%f && cp %p /mnt/server/archivedir/%f'
    #archive_timeout = 0		# force a logfile segment switch after this
                    # number of seconds; 0 disables


    #------------------------------------------------------------------------------
    # REPLICATION
    #------------------------------------------------------------------------------

    # - Sending Server(s) -

    # Set these on the master and on any standby that will send replication data.

    #max_wal_senders = 0		# max number of walsender processes
                    # (change requires restart)
    #wal_keep_segments = 0		# in logfile segments, 16MB each; 0 disables
    #wal_sender_timeout = 60s	# in milliseconds; 0 disables

    #max_replication_slots = 0	# max number of replication slots
                    # (change requires restart)
    #track_commit_timestamp = off	# collect timestamp of transaction commit
                    # (change requires restart)

    # - Master Server -

    # These settings are ignored on a standby server.

    #synchronous_standby_names = ''	# standby servers that provide sync rep
                    # comma-separated list of application_name
                    # from standby(s); '*' = all
    #vacuum_defer_cleanup_age = 0	# number of xacts by which cleanup is delayed

    # - Standby Servers -

    # These settings are ignored on a master server.

    #hot_standby = off			# "on" allows queries during recovery
                        # (change requires restart)
    #max_standby_archive_delay = 30s	# max delay before canceling queries
                        # when reading WAL from archive;
                        # -1 allows indefinite delay
    #max_standby_streaming_delay = 30s	# max delay before canceling queries
                        # when reading streaming WAL;
                        # -1 allows indefinite delay
    #wal_receiver_status_interval = 10s	# send replies at least this often
                        # 0 disables
    #hot_standby_feedback = off		# send info from standby to prevent
                        # query conflicts
    #wal_receiver_timeout = 60s		# time that receiver waits for
                        # communication from master
                        # in milliseconds; 0 disables
    #wal_retrieve_retry_interval = 5s	# time to wait before retrying to
                        # retrieve WAL after a failed attempt


    #------------------------------------------------------------------------------
    # QUERY TUNING
    #------------------------------------------------------------------------------

    # - Planner Method Configuration -

    #enable_bitmapscan = on
    #enable_hashagg = on
    #enable_hashjoin = on
    #enable_indexscan = on
    #enable_indexonlyscan = on
    #enable_material = on
    #enable_mergejoin = on
    #enable_nestloop = on
    #enable_seqscan = on
    #enable_sort = on
    #enable_tidscan = on

    # - Planner Cost Constants -

    #seq_page_cost = 1.0			# measured on an arbitrary scale
    #random_page_cost = 4.0			# same scale as above
    #cpu_tuple_cost = 0.01			# same scale as above
    #cpu_index_tuple_cost = 0.005		# same scale as above
    #cpu_operator_cost = 0.0025		# same scale as above
    effective_cache_size = 4GB

    # - Genetic Query Optimizer -

    #geqo = on
    #geqo_threshold = 12
    #geqo_effort = 5			# range 1-10
    #geqo_pool_size = 0			# selects default based on effort
    #geqo_generations = 0			# selects default based on effort
    #geqo_selection_bias = 2.0		# range 1.5-2.0
    #geqo_seed = 0.0			# range 0.0-1.0

    # - Other Planner Options -

    default_statistics_target = 100	# range 1-10000
    #constraint_exclusion = partition	# on, off, or partition
    #cursor_tuple_fraction = 0.1		# range 0.0-1.0
    #from_collapse_limit = 8
    #join_collapse_limit = 8		# 1 disables collapsing of explicit
                        # JOIN clauses


    #------------------------------------------------------------------------------
    # ERROR REPORTING AND LOGGING
    #------------------------------------------------------------------------------

    # - Where to Log -

    #log_destination = 'stderr'		# Valid values are combinations of
                        # stderr, csvlog, syslog, and eventlog,
                        # depending on platform.  csvlog
                        # requires logging_collector to be on.

    # This is used when logging to stderr:
    #logging_collector = off		# Enable capturing of stderr and csvlog
                        # into log files. Required to be on for
                        # csvlogs.
                        # (change requires restart)

    # These are only used if logging_collector is on:
    #log_directory = 'pg_log'		# directory where log files are written,
                        # can be absolute or relative to PGDATA
    #log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'	# log file name pattern,
                        # can include strftime() escapes
    #log_file_mode = 0600			# creation mode for log files,
                        # begin with 0 to use octal notation
    #log_truncate_on_rotation = off		# If on, an existing log file with the
                        # same name as the new log file will be
                        # truncated rather than appended to.
                        # But such truncation only occurs on
                        # time-driven rotation, not on restarts
                        # or size-driven rotation.  Default is
                        # off, meaning append to existing files
                        # in all cases.
    #log_rotation_age = 1d			# Automatic rotation of logfiles will
                        # happen after that time.  0 disables.
    #log_rotation_size = 10MB		# Automatic rotation of logfiles will
                        # happen after that much log output.
                        # 0 disables.

    # These are relevant when logging to syslog:
    #syslog_facility = 'LOCAL0'
    #syslog_ident = 'postgres'

    # This is only relevant when logging to eventlog (win32):
    #event_source = 'PostgreSQL'

    # - When to Log -

    #client_min_messages = notice		# values in order of decreasing detail:
                        #   debug5
                        #   debug4
                        #   debug3
                        #   debug2
                        #   debug1
                        #   log
                        #   notice
                        #   warning
                        #   error

    #log_min_messages = warning		# values in order of decreasing detail:
                        #   debug5
                        #   debug4
                        #   debug3
                        #   debug2
                        #   debug1
                        #   info
                        #   notice
                        #   warning
                        #   error
                        #   log
                        #   fatal
                        #   panic

    #log_min_error_statement = error	# values in order of decreasing detail:
                        #   debug5
                        #   debug4
                        #   debug3
                        #   debug2
                        #   debug1
                        #   info
                        #   notice
                        #   warning
                        #   error
                        #   log
                        #   fatal
                        #   panic (effectively off)

    log_min_duration_statement = 1000	# -1 is disabled, 0 logs all statements
                        # and their durations, > 0 logs only
                        # statements running at least this number
                        # of milliseconds


    # - What to Log -

    #debug_print_parse = off
    #debug_print_rewritten = off
    #debug_print_plan = off
    #debug_pretty_print = on
    #log_checkpoints = off
    #log_connections = off
    #log_disconnections = off
    #log_duration = off
    #log_error_verbosity = default		# terse, default, or verbose messages
    #log_hostname = off
    log_line_prefix = '%t [%p-%l] %q%u@%d '			# special values:
                        #   %a = application name
                        #   %u = user name
                        #   %d = database name
                        #   %r = remote host and port
                        #   %h = remote host
                        #   %p = process ID
                        #   %t = timestamp without milliseconds
                        #   %m = timestamp with milliseconds
                        #   %i = command tag
                        #   %e = SQL state
                        #   %c = session ID
                        #   %l = session line number
                        #   %s = session start timestamp
                        #   %v = virtual transaction ID
                        #   %x = transaction ID (0 if none)
                        #   %q = stop here in non-session
                        #        processes
                        #   %% = '%'
                        # e.g. '<%u%%%d> '
    log_lock_waits = on			# log lock waits >= deadlock_timeout

    #log_statement = 'none'			# none, ddl, mod, all
    #log_replication_commands = off
    #log_temp_files = -1			# log temporary files equal or larger
                        # than the specified size in kilobytes;
                        # -1 disables, 0 logs all temp files
    log_timezone = 'localtime'


    # - Process Title -

    #cluster_name = ''			# added to process titles if nonempty
                        # (change requires restart)
    #update_process_title = on


    #------------------------------------------------------------------------------
    # RUNTIME STATISTICS
    #------------------------------------------------------------------------------

    # - Query/Index Statistics Collector -

    #track_activities = on
    #track_counts = on
    #track_io_timing = off
    #track_functions = none			# none, pl, all
    #track_activity_query_size = 1024	# (change requires restart)
    stats_temp_directory = '/var/run/postgresql/9.5-main.pg_stat_tmp'


    # - Statistics Monitoring -

    #log_parser_stats = off
    #log_planner_stats = off
    #log_executor_stats = off
    #log_statement_stats = off


    #------------------------------------------------------------------------------
    # AUTOVACUUM PARAMETERS
    #------------------------------------------------------------------------------

    autovacuum = on			# Enable autovacuum subprocess?  'on'
                        # requires track_counts to also be on.
    log_autovacuum_min_duration = 0		# -1 disables, 0 logs all actions and
                        # their durations, > 0 logs only
                        # actions running at least this number
                        # of milliseconds.
    autovacuum_max_workers = 3		# max number of autovacuum subprocesses
                        # (change requires restart)
    #autovacuum_naptime = 1min		# time between autovacuum runs
    #autovacuum_vacuum_threshold = 50	# min number of row updates before
                        # vacuum
    #autovacuum_analyze_threshold = 50	# min number of row updates before
                        # analyze
    #autovacuum_vacuum_scale_factor = 0.2	# fraction of table size before vacuum
    #autovacuum_analyze_scale_factor = 0.1	# fraction of table size before analyze
    #autovacuum_freeze_max_age = 200000000	# maximum XID age before forced vacuum
                        # (change requires restart)
    #autovacuum_multixact_freeze_max_age = 400000000	# maximum multixact age
                        # before forced vacuum
                        # (change requires restart)
    autovacuum_vacuum_cost_delay = 50ms	# default vacuum cost delay for
                        # autovacuum, in milliseconds;
                        # -1 means use vacuum_cost_delay
    #autovacuum_vacuum_cost_limit = -1	# default vacuum cost limit for
                        # autovacuum, -1 means use
                        # vacuum_cost_limit


    #------------------------------------------------------------------------------
    # CLIENT CONNECTION DEFAULTS
    #------------------------------------------------------------------------------

    # - Statement Behavior -

    #search_path = '"$user", public'	# schema names
    #default_tablespace = ''		# a tablespace name, '' uses the default
    #temp_tablespaces = ''			# a list of tablespace names, '' uses
                        # only default tablespace
    #check_function_bodies = on
    #default_transaction_isolation = 'read committed'
    #default_transaction_read_only = off
    #default_transaction_deferrable = off
    #session_replication_role = 'origin'
    #statement_timeout = 0			# in milliseconds, 0 is disabled
    #lock_timeout = 0			# in milliseconds, 0 is disabled
    #vacuum_freeze_min_age = 50000000
    #vacuum_freeze_table_age = 150000000
    #vacuum_multixact_freeze_min_age = 5000000
    #vacuum_multixact_freeze_table_age = 150000000
    #bytea_output = 'hex'			# hex, escape
    #xmlbinary = 'base64'
    #xmloption = 'content'
    #gin_fuzzy_search_limit = 0
    #gin_pending_list_limit = 4MB

    # - Locale and Formatting -

    datestyle = 'iso, dmy'
    #intervalstyle = 'postgres'
    timezone = 'localtime'
    #timezone_abbreviations = 'Default'     # Select the set of available time zone
                        # abbreviations.  Currently, there are
                        #   Default
                        #   Australia (historical usage)
                        #   India
                        # You can create your own file in
                        # share/timezonesets/.
    #extra_float_digits = 0			# min -15, max 3
    #client_encoding = sql_ascii		# actually, defaults to database
                        # encoding

    # These settings are initialized by initdb, but they can be changed.
    lc_messages = 'ru_RU.UTF-8'			# locale for system error message
                        # strings
    lc_monetary = 'ru_RU.UTF-8'			# locale for monetary formatting
    lc_numeric = 'ru_RU.UTF-8'			# locale for number formatting
    lc_time = 'ru_RU.UTF-8'				# locale for time formatting

    # default configuration for text search
    default_text_search_config = 'pg_catalog.russian'

    # - Other Defaults -

    #dynamic_library_path = '$libdir'
    #local_preload_libraries = ''
    #session_preload_libraries = ''


    #------------------------------------------------------------------------------
    # LOCK MANAGEMENT
    #------------------------------------------------------------------------------

    #deadlock_timeout = 1s
    #max_locks_per_transaction = 64		# min 10
                        # (change requires restart)
    # Note:  Each lock table slot uses ~270 bytes of shared memory, and there are
    # max_locks_per_transaction * (max_connections + max_prepared_transactions)
    # lock table slots.
    #max_pred_locks_per_transaction = 64	# min 10
                        # (change requires restart)


    #------------------------------------------------------------------------------
    # VERSION/PLATFORM COMPATIBILITY
    #------------------------------------------------------------------------------

    # - Previous PostgreSQL Versions -

    #array_nulls = on
    #backslash_quote = safe_encoding	# on, off, or safe_encoding
    #default_with_oids = off
    #escape_string_warning = on
    #lo_compat_privileges = off
    #operator_precedence_warning = off
    #quote_all_identifiers = off
    #sql_inheritance = on
    #standard_conforming_strings = on
    #synchronize_seqscans = on

    # - Other Platforms and Clients -

    #transform_null_equals = off


    #------------------------------------------------------------------------------
    # ERROR HANDLING
    #------------------------------------------------------------------------------

    #exit_on_error = off			# terminate session on any error?
    #restart_after_crash = on		# reinitialize after backend crash?


    #------------------------------------------------------------------------------
    # CONFIG FILE INCLUDES
    #------------------------------------------------------------------------------

    # These options allow settings to be loaded from files other than the
    # default postgresql.conf.

    #include_dir = 'conf.d'			# include files ending in '.conf' from
                        # directory 'conf.d'
    #include_if_exists = 'exists.conf'	# include file only if it exists
    #include = 'special.conf'		# include file




Список и версии python пакетов
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

django и прочие пакеты python следует устанвливать утилитой **pip** с указанием версий.

Не все пакеты из списка ниже необходимы для базовых функций проекта.

 ::

    root@iss:/srv/django/iss# pip list
    alabaster (0.7.9)
    Babel (2.3.4)
    decorator (4.0.10)
    Django (1.9.6)
    docutils (0.12)
    easysnmp (0.2.4)
    gunicorn (19.4.5)
    imagesize (0.7.1)
    ipython (2.4.1)
    Jinja2 (2.8)
    lorem-ipsum-generator (0.3)
    MarkupSafe (0.23)
    MySQL-python (1.2.5)
    mysqlclient (1.3.7)
    netsnmp-python (1.0a1)
    networkx (1.11)
    pexpect (4.0.1)
    pip (9.0.1)
    ply (3.9)
    psycopg2 (2.6.2)
    ptyprocess (0.5)
    pyasn1 (0.1.9)
    pycrypto (2.6.1)
    Pygments (2.1.3)
    pymssql (2.1.3)
    pysmi (0.0.7)
    pysnmp (4.3.2)
    pysnmp-mibs (0.1.6)
    pytz (2016.6.1)
    requests (2.11.1)
    setuptools (20.7.0)
    simplegeneric (0.8.1)
    six (1.10.0)
    snowballstemmer (1.2.1)
    Sphinx (1.4.6)
    tabulate (0.7.7)
    transliterate (1.8.1)
    wheel (0.29.0)
    yolk (0.4.3)



Настройка статики
-----------------

Файл settings.py
~~~~~~~~~~~~~~~~

 ::

    STATIC_URL = 'http://10.6.0.22:10000/static/admin/'

    ROOT_URL = '/'

    MY_STATIC_URL = 'http://10.6.0.22:10000/'


nginx файл /etc/nginx/iss
~~~~~~~~~~~~~~~~~~~~~~~~~

 ::

    server {
            listen        10000;
            server_name   10.6.0.22;

            root /srv/django/iss/static;
            index index.html;

            location / {
                add_header Access-Control-Allow-Origin *;
                autoindex on;
            }

            location /static/admin {
                alias /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/;
                autoindex on;
            }

    }



Подключение к базам данных (файл dbconn.py)
-------------------------------------------

 ::

    DATABASES = {

        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'iss',
            'USER': 'iss',
            'PASSWORD':'*******',
        },

        'zenoss_krsk' : {
            'ENGINE':'django.db.backends.mysql',
            'NAME':'zenoss_zep',
            'USER':'iss',
            'PASSWORD':'*******',
            'HOST':'10.6.0.129',
            'PORT':'',
        },


    }



    ONYMA_USERNAME = 'iss2'
    ONYMA_PASSWORD = '********'


    ISS_MSSQL_USERNAME = "django"
    ISS_MSSQL_PASSWORD = "*********"


    ZENOSS_API_USERNAME = "vkomarov"
    ZENOSS_API_PASSWORD = "********"



Создание структуры данных
-------------------------

 ::

    cd /srv/django/iss
    python manage.py makemigrations
    python manage.py migrate



Перенос данных
~~~~~~~~~~~~~~

#. Способ : используя штатные средства создания резервных копий и загрузки сервера баз данных
#. Способ : использую штатные средства django - dumpdata и loaddata


Общие рекомендации по переносу миграций (из 6-ти шагов)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#. delete from django_migrations; (sql server)
#. rm -f <app>/migrations/*
#. python manage.py migrate --fake
#. python manage.py makemigrations
#. python manage.py migrate --fake-initial
#. python manage.py migrate



Запуск проекта в режиме использования собственного сервера
----------------------------------------------------------

 ::

    cd /srv/django/iss
    python manage.py runserver


Backup files
------------


.. warning:: Данные формата json должны соответствовать структуре моделей.



Установка и настройка memcachedb
--------------------------------


Установка
~~~~~~~~~
 ::

    #apt-get install memcachedb


Подключение к django
~~~~~~~~~~~~~~~~~~~~

Добавить параметр в settings.py

 ::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:21201',
        }
    }


.. warning:: Необходимо убедиться, то memcachedb принимает запросы по указанному в **CACHES** адресу и порту.






.. index:: gunicorn

Использование gunicorn
----------------------


gunicorn
~~~~~~~~

**root@iss:/etc# cat /etc/gunicorn.d/iss.conf**

 ::

    CONFIG = {
        'working_dir': '/srv/django/iss',
        'args': (
            '--bind=127.0.0.1:5000',
            '--workers=4',
            '--timeout=260',
            '--max-requests=500',
            '--reload',
            'iss.wsgi',
            'iss.wsgi:application',
            #'--log-level=debug',
        ),
    }


nginx
~~~~~

**root@iss:/etc/nginx# cat /etc/nginx/sites-available/iss**

 ::

    server {
            listen        10000;
            server_name   10.6.0.22;

        root /srv/django/iss/static;
        index index.html;

        location / {
            add_header Access-Control-Allow-Origin *;
            autoindex on;
        }

        location /static/admin {
            alias /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/;
            autoindex on;
        }



    }


    server {

            listen        8000;
            server_name   10.6.0.22;


        location / {
                include proxy_params;
                proxy_pass http://127.0.0.1:5000;
        }


        location /doc {
            alias /srv/django/iss/doc/build/html/;
            index index.html;
            autoindex on;
        }


    }

Управление
~~~~~~~~~~

Пример:

 ::

    root@iss:/etc/nginx# systemctl status gunicorn
    ● gunicorn.service
       Loaded: loaded (/etc/init.d/gunicorn; bad; vendor preset: enabled)
       Active: active (running) since Чт 2017-03-02 21:36:48 +07; 11h ago
         Docs: man:systemd-sysv-generator(8)
        Tasks: 9
       Memory: 138.8M
          CPU: 21min 5.808s
       CGroup: /system.slice/gunicorn.service
               ├─30097 /usr/bin/python /usr/bin/gunicorn --pid /var/run/gunicorn/iss.conf.pid --name iss.conf --user www-data --group www-data --daemon --log-file /var/log/gunic
               ├─30102 /usr/bin/python /usr/bin/gunicorn --pid /var/run/gunicorn/iss.conf.pid --name iss.conf --user www-data --group www-data --daemon --log-file /var/log/gunic
               ├─30106 /usr/bin/python /usr/bin/gunicorn --pid /var/run/gunicorn/iss.conf.pid --name iss.conf --user www-data --group www-data --daemon --log-file /var/log/gunic
               ├─30108 /usr/bin/python /usr/bin/gunicorn --pid /var/run/gunicorn/iss.conf.pid --name iss.conf --user www-data --group www-data --daemon --log-file /var/log/gunic
               └─30110 /usr/bin/python /usr/bin/gunicorn --pid /var/run/gunicorn/iss.conf.pid --name iss.conf --user www-data --group www-data --daemon --log-file /var/log/gunic

    мар 02 21:36:47 iss systemd[1]: Stopped gunicorn.service.
    мар 02 21:36:47 iss systemd[1]: Starting gunicorn.service...
    мар 02 21:36:47 iss gunicorn[30088]:  * Starting Gunicorn workers
    мар 02 21:36:48 iss gunicorn[30088]:  [iss.conf] *
    мар 02 21:36:48 iss systemd[1]: Started gunicorn.service.


