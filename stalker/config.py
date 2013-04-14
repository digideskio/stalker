# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
# 
# This file is part of Stalker.
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import os
import datetime
import logging
import tempfile

logger = logging.getLogger(__name__)


class Config(object):
    """Config abstraction
    
    Idea is coming from Sphinx config.
    
    Holds system wide configuration variables. See
    `configuring stalker`_ for more detail.
    
    .. _configuring stalker: ../configure.html
    """
    
    default_config_values = dict(
        
        #
        # The default settings for the database, see sqlalchemy.create_engine
        # for possible parameters
        # 
        database_engine_settings = {
            "sqlalchemy.url": "sqlite:///:memory:",
            "sqlalchemy.echo": False,
        },
        
        database_session_settings = {},
        
        
        #
        # Tells Stalker to create an admin by default
        #
        auto_create_admin = True,
        
        # 
        # these are for new projects
        # after creating the project you can change them from the interface
        # 
        admin_name = 'admin',
        admin_login = 'admin',
        admin_code = 'adm',
        admin_password = 'admin',
        admin_email = 'admin@admin.com',
        admin_department_name = 'admins',
        admin_group_name = 'admins',
        
        # the default keyword which is going to be used in password scrambling
        key = "stalker_default_key",
        
        version_take_name = "Main",

        ticket_label = "Ticket",
        
        actions = ['Create', 'Read', 'Update', 'Delete', 'List'], #CRUDL
        
        status_bg_color = 0xffffff,
        status_fg_color = 0x000000,
        
        # Tickets

        # define the available actions per Status
        ticket_status_order = [
            'new', 'accepted', 'assigned', 'reopened', 'closed'
        ],
        
        ticket_resolutions = [
            'fixed', 'invalid', 'wontfix', 'duplicate', 'worksforme', 'cantfix'
        ],
        
        ticket_workflow = {
            'resolve' : {
                'new': {
                    'new_status': 'closed',
                    'action': 'set_resolution'
                },
                'accepted': {
                    'new_status': 'closed',
                    'action': 'set_resolution'
                },
                'assigned': {
                    'new_status': 'closed',
                    'action': 'set_resolution'
                },
                'reopened': {
                    'new_status': 'closed',
                    'action': 'set_resolution'
                },
            },
            'accept' : {
                'new': {
                    'new_status': 'accepted',
                    'action': 'set_owner'
                },
                'accepted': {
                    'new_status': 'accepted',
                    'action': 'set_owner'
                },
                'assigned': {
                    'new_status': 'accepted',
                    'action': 'set_owner'
                },
                'reopened': {
                    'new_status': 'accepted',
                    'action': 'set_owner'
                },
            },
            'reassign': {
                'new': {
                    'new_status': 'assigned',
                    'action': 'set_owner'
                },
                'accepted': {
                    'new_status': 'assigned',
                    'action': 'set_owner'
                },
                'assigned': {
                    'new_status': 'assigned',
                    'action': 'set_owner'
                },
                'reopened': {
                    'new_status': 'assigned',
                    'action': 'set_owner'
                },
            },
            'reopen': {
                'closed': {
                    'new_status': 'reopened',
                    'action': 'del_resolution'
                }
            }
        },
         
        # Task Management
        timing_resolution = datetime.timedelta(hours=1),
        task_duration = datetime.timedelta(days=10),
        task_priority = 500,
        
        working_hours = {
          'mon': [[570, 1110]], # 9:30 - 18:30
          'tue': [[570, 1110]], # 9:30 - 18:30
          'wed': [[570, 1110]], # 9:30 - 18:30
          'thu': [[570, 1110]], # 9:30 - 18:30
          'fri': [[570, 1110]], # 9:30 - 18:30
          'sat': [], # saturday off
          'sun': [], # sunday off
        },
        
        day_order = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'],
        
        daily_working_hours = 8,
        
        datetime_units = ['min', 'h', 'd', 'w', 'm', 'y'],
        
        task_schedule_models = ['effort', 'length', 'duration'],
        
        task_schedule_constraints = ['none', 'start', 'end', 'both'],
        
        tjp_working_hours_template = """{% macro wh(wh, day) -%}
        {%- if wh[day]|length %}    workinghours {{day}} {% for part in wh[day] -%}
                {%- if loop.index != 1%}, {% endif -%}
                {{"%02d"|format(part[0]//60)}}:{{"%02d"|format(part[0]%60)}} - {{"%02d"|format(part[1]//60)}}:{{"%02d"|format(part[1]%60)}}
                {%- endfor -%}
        {%- else %}    workinghours {{day}} off
        {%- endif -%}
        {%- endmacro -%}
        {{wh(workinghours, 'mon')}}
        {{wh(workinghours, 'tue')}}
        {{wh(workinghours, 'wed')}}
        {{wh(workinghours, 'thu')}}
        {{wh(workinghours, 'fri')}}
        {{wh(workinghours, 'sat')}}
        {{wh(workinghours, 'sun')}}""",
        
        tjp_project_template = """project {{ project.tjp_id }} "{{ project.name }}" {{ project.start.date() }} - {{ project.end.date() }} {
            timingresolution {{ '%i'|format(project.timing_resolution.total_seconds()//60|int) }}min
            now {{ now }}
            dailyworkinghours {{ project.daily_working_hours }}
            weekstartsmonday
        {{ project.working_hours.to_tjp }}
            timeformat "%Y-%m-%d"
            scenario plan "Plan"
            trackingscenario plan
        }
        """,
        
        tjp_task_template = """task {{task.tjp_id}} "{{task.name}}" {
        {%- if task.is_container -%}
            {%- for child_task in task.children %}
        {{ child_task.to_tjp }}
            {%- endfor %}
        {%- else %}
            {{task.schedule_model}} {{task.schedule_timing}}{{task.schedule_unit}}
            allocate {% for resource in task.resources -%}
                {%-if loop.index != 1 %}, {% endif %}{{resource.tjp_id}}
            {%- endfor %}
            {%- if task.depends %}
            depends {% for depends in task.depends %}
                {%- if loop.index != 1 %}, {% endif %}{{depends.tjp_abs_id}}
            {%- endfor -%}
            {%- endif -%}
        {% endif %}
        }
        """,
                
                tjp_department_template = '''resource {{department.tjp_id}} "{{department.name}}" {
        {%- for resource in department.users %}
            {{resource.to_tjp}}
        {%- endfor %}
        }''',
        
        tjp_user_template = '''resource {{user.tjp_id}} "{{user.name}}"''',
        
        tjp_main_template = """# Generated By Stalker v{{stalker.__version__}}
        {{project.to_tjp}}
            
        # resources
        resource resources "Resources" {
        {%- for user in users %}
            {{user.to_tjp}}
        {%- endfor %}
        }
        
        # tasks
        task {{project.tjp_id}} "{{project.name}}"{
            {% for task in project.root_tasks %}
            {{task.to_tjp}}
            {% endfor %}
        }
        
        # bookings
        
        # reports
        taskreport breakdown "{{csv_file_full_path}}"{
            formats csv
            timeformat "%Y-%m-%d-%H:%M"
            columns id, start, end
        }
        """,
        
        tj_command = '/usr/local/bin/tj3',
        
        # --------------------------------------------
        # following coming from oyProjectManager 
        sequence_format = "%h%p%t %R",
        file_size_format = "%.2f MB",
        time_format = '%d.%m.%Y %H:%M',
        
        resolution_presets = {
            "PC Video": [640, 480, 1.0],
            "NTSC": [720, 486, 0.91],
            "NTSC 16:9": [720, 486, 1.21],
            "PAL": [720, 576, 1.067],
            "PAL 16:9": [720, 576, 1.46],
            "HD 720": [1280, 720, 1.0],
            "HD 1080": [1920, 1080, 1.0],
            "1K Super 35": [1024, 778, 1.0],
            "2K Super 35": [2048, 1556, 1.0],
            "4K Super 35": [4096, 3112, 1.0],
            "A4 Portrait": [2480, 3508, 1.0],
            "A4 Landscape": [3508, 2480, 1.0],
            "A3 Portrait": [3508, 4960, 1.0],
            "A3 Landscape": [4960, 3508, 1.0],
            "A2 Portrait": [4960, 7016, 1.0],
            "A2 Landscape": [7016, 4960, 1.0],
            "50x70cm Poster Portrait": [5905, 8268, 1.0],
            "50x70cm Poster Landscape": [8268, 5905, 1.0],
            "70x100cm Poster Portrait": [8268, 11810, 1.0],
            "70x100cm Poster Landscape": [11810, 8268, 1.0],
            "1k Square": [1024, 1024, 1.0],
            "2k Square": [2048, 2048, 1.0],
            "3k Square": [3072, 3072, 1.0],
            "4k Square": [4096, 4096, 1.0],
        },
        
        default_resolution_preset = "HD 1080",
        
        project_structure = """{% for shot in project.shots %}
                Shots/{{shot.code}}
                Shots/{{shot.code}}/Plate
                Shots/{{shot.code}}/Reference
                Shots/{{shot.code}}/Texture
            {% endfor %}
        {% for asset in project.assets%}
            {% set asset_path = project.full_path + '/Assets/' + asset.type.name + '/' + asset.code %}
            {{asset_path}}/Texture
            {{asset_path}}/Reference
        {% endfor %}
        """,
        
        thumbnail_format = "jpg",
        thumbnail_quality = 70,
        thumbnail_size = [320, 180],
        
        server_local_storage = os.path.join(tempfile.gettempdir(), 'Stalker')
        
    )

    def __init__(self):
        
        self.config_values = Config.default_config_values.copy()
        self.user_config = {}
        
        # the priority order is
        # stalker.config
        # config.py under .stalker_rc directory
        # config.py under $STALKER_PATH
        
        self._parse_settings()
    
    def _parse_settings(self):
        # for now just use $STALKER_PATH
        ENV_KEY = "STALKER_PATH"
        
        # try to get the environment variable
        if not os.environ.has_key(ENV_KEY):
            # don't do anything
            logger.debug("no environment key found for user settings")
        else:
            logger.debug("environment key found")
            
            resolved_path = os.path.expanduser(
                os.path.join(
                    os.environ[ENV_KEY],
                    "config.py"
                )
            )
            
            # using `while` is not safe to expand variables
            # do the expansion for 5 times which is complex enough
            # and I don't (hopefully) expect anybody to use
            # more than 5 level deep environment variables
            resolved_path = os.path.expandvars(
                os.path.expandvars(
                    os.path.expandvars(
                        os.path.expandvars(
                            resolved_path
                        )
                    )
                )
            )
            
            try:
                try:
                    logger.debug("importing user config")
                    execfile(resolved_path, self.user_config)
                except SyntaxError, err:
                    raise RuntimeError("There is a syntax error in your "
                                       "configuration file: " + str(err))
                
                # append the data to the current settings
                logger.debug("updating system config")
                for key in self.user_config:
                    #if key in self.config_values:
                    self.config_values[key] = self.user_config[key]
            
            except IOError:
                logger.warning("The $STALKER_PATH:" + resolved_path + \
                               " doesn't exists! skipping user config")
    
    def __getattr__(self, name):
        return self.config_values[name]
    
    def __getitem__(self, name):
        return getattr(self, name)
    
    def __setitem__(self, name, value):
        return setattr(self, name, value)
    
    def __delitem__(self, name):
        delattr(self, name)
    
    def __contains__(self, name):
        return name in self.config_values