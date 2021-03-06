# Licensed to the Encore Technologies ("Encore") under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from menandmice.base import BaseObject
from menandmice.base import BaseService


class Role(BaseObject):
    def __init__(self, *args, **kwargs):
        super(Role, self).__init__(*args, **kwargs)
        self.add_key('ref')
        self.add_key('name')
        self.add_key('description')
        self.add_key('users', [])  # list of User()
        self.add_key('groups', [])  # list of Group()


class User(BaseObject):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.add_key('ref')
        self.add_key('name')
        self.add_key('password')
        self.add_key('fullName')
        self.add_key('description')
        self.add_key('email')
        self.add_key('authenticationType')
        self.add_key('roles', [])  # list of Role()
        self.add_key('groups', [])  # list of Group()


class Group(BaseObject):
    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        self.add_key('ref')
        self.add_key('name')
        self.add_key('description')
        self.add_key('adIntegrated')
        self.add_key('groupMembers', [])   # list of User()
        self.add_key('roles', [])   # list of Role()


class Groups(BaseService):
    def __init__(self, client):
        super(Groups, self).__init__(client=client,
                                     url_base="Groups",
                                     entity_class=Group,
                                     get_response_entity_key="group",
                                     get_response_all_key="groups")

    def add(self, group_input, save_comment=""):
        payload = {
            "saveComment": save_comment,
            "group": group_input
        }
        group_json = self.client.post("{0}{1}".format(self.client.baseurl,
                                                      self.url_base),
                                      payload)
        group_return = []
        for ref in group_json['result']['objRefs']:
            group_return.append(self.get(ref)[0])
        return group_return

    def get_group_roles(self, group, **kwargs):
        group_ref = self.ref_or_raise(group)
        all_roles = []
        query_string = self.make_query_str(**kwargs)
        role_response = self.client.get("{0}{1}/Roles{2}".format(self.client.baseurl,
                                                                 group_ref,
                                                                 query_string))
        for role in role_response['result']['roles']:
            all_roles.append(Role(role))
        return all_roles

    def delete_group_role(self, group, role, save_comment=""):
        group_ref = self.ref_or_raise(group)
        role_ref = self.ref_or_raise(role)
        if save_comment:
            save_comment = self.make_query_str(**{"saveComment": save_comment})
        return self.client.delete("{0}{1}/{2}{3}".format(self.client.baseurl,
                                                         group_ref,
                                                         role_ref,
                                                         save_comment))

    def add_group_role(self, group, role, save_comment=""):
        group_ref = self.ref_or_raise(group)
        role_ref = self.ref_or_raise(role)
        payload = {
            "saveComment": save_comment
        }
        return self.client.put("{0}{1}/{2}".format(self.client.baseurl,
                                                   group_ref,
                                                   role_ref),
                               payload,
                               True)

    def get_group_users(self, group, **kwargs):
        group_ref = self.ref_or_raise(group)
        all_users = []
        query_string = self.make_query_str(**kwargs)
        role_response = self.client.get("{0}{1}/Users{2}".format(self.client.baseurl,
                                                                 group_ref,
                                                                 query_string))
        for user in role_response['result']['users']:
            all_users.append(User(user))
        return all_users

    def delete_group_user(self, group, user, save_comment=""):
        group_ref = self.ref_or_raise(group)
        user_ref = self.ref_or_raise(user)
        if save_comment:
            save_comment = self.make_query_str(**{"saveComment": save_comment})
        return self.client.delete("{0}{1}/{2}{3}".format(self.client.baseurl,
                                                         group_ref,
                                                         user_ref,
                                                         save_comment))

    def add_group_user(self, group, user, save_comment=""):
        group_ref = self.ref_or_raise(group)
        user_ref = self.ref_or_raise(user)
        payload = {
            "saveComment": save_comment
        }
        return self.client.put("{0}{1}/{2}".format(self.client.baseurl,
                                                   group_ref,
                                                   user_ref),
                               payload,
                               True)


class Roles(BaseService):
    def __init__(self, client):
        super(Roles, self).__init__(client=client,
                                    url_base="Roles",
                                    entity_class=Role,
                                    get_response_entity_key="role",
                                    get_response_all_key="roles")

    def add(self, role, save_comment=""):
        payload = {
            "saveComment": save_comment,
            "role": role
        }
        role_json = self.client.post("{0}{1}".format(self.client.baseurl,
                                                     self.url_base),
                                     payload)
        role_return = []
        for ref in role_json['result']['objRefs']:
            role_return.append(self.get(ref)[0])
        return role_return

    def get_role_groups(self, role, **kwargs):
        role_ref = self.ref_or_raise(role)
        all_groups = []
        query_string = self.make_query_str(**kwargs)
        group_response = self.client.get("{0}{1}/Groups{2}".format(self.client.baseurl,
                                                                   role_ref,
                                                                   query_string))
        for group in group_response['result']['groups']:
            all_groups.append(Group(group))
        return all_groups

    def get_role_users(self, role, **kwargs):
        role_ref = self.ref_or_raise(role)
        all_users = []
        query_string = self.make_query_str(**kwargs)
        user_response = self.client.get("{0}{1}/Users{2}".format(self.client.baseurl,
                                                                 role_ref,
                                                                 query_string))
        for user in user_response['result']['users']:
            all_users.append(User(user))
        return all_users


class Users(BaseService):
    def __init__(self, client):
        super(Users, self).__init__(client=client,
                                    url_base="Users",
                                    entity_class=User,
                                    get_response_entity_key="user",
                                    get_response_all_key="users")

    def add(self, user, save_comment=""):
        payload = {
            "saveComment": save_comment,
            "user": user
        }
        user_json = self.client.post("{0}{1}".format(self.client.baseurl,
                                                     self.url_base),
                                     payload)
        user_return = []
        for ref in user_json['result']['objRefs']:
            user_return.append(self.get(ref)[0])
        return user_return

    def get_user_groups(self, user, **kwargs):
        user_ref = self.ref_or_raise(user)
        all_groups = []
        query_string = self.make_query_str(**kwargs)
        group_response = self.client.get("{0}{1}/Groups{2}".format(self.client.baseurl,
                                                                   user_ref,
                                                                   query_string))
        for group in group_response['result']['groups']:
            all_groups.append(Group(group))
        return all_groups

    def get_user_roles(self, user, **kwargs):
        user_ref = self.ref_or_raise(user)
        all_roles = []
        query_string = self.make_query_str(**kwargs)
        role_response = self.client.get("{0}{1}/Roles{2}".format(self.client.baseurl,
                                                                 user_ref,
                                                                 query_string))
        for role in role_response['result']['roles']:
            all_roles.append(Role(role))
        return all_roles

    def delete_user_role(self, user, role, save_comment=""):
        user_ref = self.ref_or_raise(user)
        role_ref = self.ref_or_raise(role)
        if save_comment:
            save_comment = self.make_query_str(**{"saveComment": save_comment})
        return self.client.delete("{0}{1}/{2}{3}".format(self.client.baseurl,
                                                         user_ref,
                                                         role_ref,
                                                         save_comment))

    def add_user_role(self, user, role, save_comment=""):
        user_ref = self.ref_or_raise(user)
        role_ref = self.ref_or_raise(role)
        payload = {
            "saveComment": save_comment
        }
        return self.client.put("{0}{1}/{2}".format(self.client.baseurl,
                                                   user_ref,
                                                   role_ref),
                               payload,
                               True)
