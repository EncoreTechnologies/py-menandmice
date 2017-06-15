import requests
import json

from menandmice.Base import BaseObject

from menandmice.dns import DNSGenerateDirective
from menandmice.dns import DNSRecords
from menandmice.dns import DNSView
from menandmice.dns import DNSViews
from menandmice.dns import DNSZone
from menandmice.dns import DNSZoneOptions
from menandmice.dns import DNSZones

from menandmice.ipam import AddressBlock
from menandmice.ipam import ChangeRequest
from menandmice.ipam import ChangeRequests
from menandmice.ipam import Device
from menandmice.ipam import Devices
from menandmice.ipam import Discovery
from menandmice.ipam import Folder
from menandmice.ipam import Folders
from menandmice.ipam import GetRangeStatisticsResponse
from menandmice.ipam import Interface
from menandmice.ipam import Interfaces
from menandmice.ipam import IPAMRecord
from menandmice.ipam import IPAMRecords
from menandmice.ipam import Range
from menandmice.ipam import Ranges

from menandmice.users import Group
from menandmice.users import Groups
from menandmice.users import Role
from menandmice.users import Roles
from menandmice.users import User
from menandmice.users import Users


class ObjectAccess(BaseObject):
    def __init__(self, **kwargs):
        self.ref = self.get_value('ref', **kwargs)
        self.name = self.get_value('name', **kwargs)
        self.identityAccess = self.build_obj_list(IdentityAccess,
                                                  self.get_value('identityAccess', **kwargs))


class IdentityAccess(BaseObject):
    def __init__(self, **kwargs):
        self.identityRef = self.get_value('identityRef', **kwargs)
        self.identityName = self.get_value('identityName', **kwargs)
        self.accessEntries = self.buildAccessEntries(
            self.get_value('accessEntries', **kwargs))

    def buildAccessEntries(self, accessEntries):
        all_accessEntries = []
        if accessEntries:
            if isinstance(accessEntries, list):
                for entry in accessEntries:
                    all_accessEntries.append(AccessEntry(**entry))
            else:
                all_accessEntries.append(AccessEntry(**accessEntries))
        return all_accessEntries


class AccessEntry(BaseObject):
    def __init__(self, **kwargs):
        self.name = self.get_value('name', **kwargs)
        self.access = self.get_value('access', **kwargs)


class Event(BaseObject):
    def __init__(self, **kwargs):
        self.eventType = self.get_value('eventType', **kwargs)
        self.objType = self.get_value('objType', **kwargs)
        self.objRef = self.get_value('objRef', **kwargs)
        self.objName = self.get_value('objName', **kwargs)
        self.timestamp = self.get_value('timestamp', **kwargs)
        self.username = self.get_value('username', **kwargs)
        self.saveComment = self.get_value('saveComment', **kwargs)
        self.eventText = self.get_value('eventText', **kwargs)


class PropertyDefinition(BaseObject):
    def __init__(self, **kwargs):
        self.name = self.get_value('name', **kwargs)
        self.type = self.get_value('type', **kwargs)
        self.system = self.get_value('system', **kwargs)
        self.mandatory = self.get_value('mandatory', **kwargs)
        self.readOnly = self.get_value('readOnly', **kwargs)
        self.multiLine = self.get_value('multiLine', **kwargs)
        self.defaultValue = self.get_value('defaultValue', **kwargs)
        self.listItems = self.get_value('listItems', **kwargs)
        self.parentProperty = self.get_value('parentProperty', **kwargs)


class Client(BaseObject):
    def __init__(self, server, username, password):
        self.baseurl = "http://{0}/mmws/api/".format(server)
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.DNSZones = DNSZones(self)
        self.DNSRecords = DNSRecords(self)
        self.DNSViews = DNSViews(self)
        self.Folders = Folders(self)
        self.Users = Users(self)
        self.Groups = Groups(self)
        self.Roles = Roles(self)
        self.IPAMRecords = IPAMRecords(self)
        self.Ranges = Ranges(self)
        self.Interfaces = Interfaces(self)
        self.Devices = Devices(self)
        self.ChangeRequests = ChangeRequests(self)

    def newDnsZone(self, **kwargs):
        return DNSZone(**kwargs)

    def newDnsRecord(self, **kwargs):
        return DNSRecords(**kwargs)

    def newDnsView(self, **kwargs):
        return DNSView(**kwargs)

    def newDnsGenerateDirective(self, **kwargs):
        return DNSGenerateDirective(**kwargs)

    def newDnsZoneOptions(self, **kwargs):
        return DNSZoneOptions(**kwargs)

    def newFolder(self, **kwargs):
        return Folder(**kwargs)

    def newObjectAccess(self, **kwargs):
        return ObjectAccess(**kwargs)

    def newIdentityAccess(self, **kwargs):
        return IdentityAccess(**kwargs)

    def newAccessEntry(self, **kwargs):
        return AccessEntry(**kwargs)

    def newEvent(self, **kwargs):
        return Event(**kwargs)

    def newPropertyDefinition(self, **kwargs):
        return PropertyDefinition(**kwargs)

    def newRole(self, **kwargs):
        return Role(**kwargs)

    def newGroup(self, **kwargs):
        return Group(**kwargs)

    def newUser(self, **kwargs):
        return User(**kwargs)

    def newIpamRecord(self, **kwargs):
        return IPAMRecord(**kwargs)

    def newRange(self, **kwargs):
        return Range(**kwargs)

    def newDiscovery(self, **kwargs):
        return Discovery(**kwargs)

    def newAddressBlock(self, **kwargs):
        return AddressBlock(**kwargs)

    def newRangeStatisticsResponse(self, **kwargs):
        return GetRangeStatisticsResponse(**kwargs)

    def newInterface(self, **kwargs):
        return Interface(**kwargs)

    def newDevice(self, **kwargs):
        return Device(**kwargs)

    def newChangeRequest(self, **kwargs):
        return ChangeRequest(**kwargs)

    def sanitize_json(self, json_obj):
        for k, v in json_obj.items():
            if v is None:
                del json_obj[k]
            elif not v:
                del json_obj[k]
            elif isinstance(v, list):
                for list_value in v:
                    self.sanitize_json(list_value)
            elif isinstance(v, dict):
                self.sanitize_json(v)
        return json_obj

    def get(self, url):
        print(url)
        response = self.session.get(url)
        return_val = ""
        print(response.status_code)
        if response.status_code == 200:
            return_val = response.json()
        elif response.status_code == 204:
            return_val = "No data to display"
        else:
            error_json = response.json()
            if error_json:
                code = error_json['error']['code']
                message = error_json['error']['message']
                raise requests.exceptions.HTTPError(
                    "{0}: {1}".format(code, message))
            else:
                response.raise_for_status()
        return return_val

    def post(self, url, payload):
        sanitized_payload = self.sanitize_json(payload)
        print(sanitized_payload)
        response = self.session.post(url, json=sanitized_payload)
        if response.status_code != 201:
            error_json = response.json()
            if error_json:
                code = error_json['error']['code']
                message = error_json['error']['message']
                raise requests.exceptions.HTTPError(
                    "{0}: {1}".format(code, message))
            else:
                response.raise_for_status()
        return response.json()

    def delete(self, url):
        response = self.session.delete(url)
        return_status = ""
        if response.status_code == 204:
            return_status = "Successfully removed!"
        else:
            error_json = response.json()
            if error_json:
                code = error_json['error']['code']
                message = error_json['error']['message']
                raise requests.exceptions.HTTPError(
                    "{0}: {1}".format(code, message))
            else:
                response.raise_for_status()
        return return_status

    def put(self, url, payload, sanitize_override=False):
        print(url)
        if not sanitize_override:
            payload = self.sanitize_json(payload)
        print(payload)
        response = self.session.put(url, json=payload)
        return_status = ""
        if response.status_code == 204:
            return_status = "Successfully updated!"
        else:
            error_json = response.json()
            if error_json:
                code = error_json['error']['code']
                message = error_json['error']['message']
                raise requests.exceptions.HTTPError(
                    "{0}: {1}".format(code, message))
            else:
                response.raise_for_status()
        return return_status

    def deleteItem(self, ref, **kwargs):
        query_string = self.make_query_str(**kwargs)
        return self.delete("{0}{1}{2}".format(self.baseurl, ref, query_string))

    def updateItem(self, ref, properties, objType, saveComment, deleteUnspecified):
        if not isinstance(properties, list):
            properties = [properties]
        payload = {
            "ref": ref,
            "objType": objType,
            "saveComment": saveComment,
            "deleteUnspecified": deleteUnspecified,
            "properties": properties
        }
        return self.put("{0}{1}".format(self.baseurl, ref), payload)

    def buildAccess(self, json_input):
        return self.json_to_class(json_input, ObjectAccess)

    def getItemAccess(self, ref, **kwargs):
        query_string = self.make_query_str(**kwargs)
        access_response_json = self.get(
            "{0}{1}/Access{2}".format(self.baseurl, ref, query_string))
        access_object = self.buildAccess(
            access_response_json['result']['objectAccess'])
        return access_object

    def setItemAccess(self, ref, identity_access, object_type, saveComment):
        if isinstance(identity_access, IdentityAccess):
            identity_access = json.loads(identity_access.to_json())
        if not isinstance(identity_access, list):
            identity_access = [identity_access]
        payload = {
            "objType": object_type,
            "saveComment": saveComment,
            "identityAccess": identity_access
        }
        print(payload)
        return self.put("{0}{1}/Access".format(self.baseurl, ref), payload)

    def buildEvent(self, json_input):
        return self.json_to_class(json_input, Event)

    def getItemHistory(self, ref, **kwargs):
        query_string = self.make_query_str(**kwargs)
        history_response_json = self.get(
            "{0}{1}/History{2}".format(self.baseurl, ref, query_string))
        all_events = []
        for event in history_response_json['result']['events']:
            all_events.append(self.buildEvent(event))
        return all_events

    def buildDefinition(self, json_input):
        return self.json_to_class(json_input, PropertyDefinition)

    def getPropertyDefinitions(self, ref, property_name):
        url = ""
        if property_name:
            url = "{0}{1}/PropertyDefinitions/{2}".format(
                self.baseurl, ref, property_name)
        else:
            url = "{0}{1}/PropertyDefinitions".format(self.baseurl, ref)
        property_definitions_json = self.get(url)
        property_definitions = []
        for definition in property_definitions_json['result']['propertyDefinitions']:
            property_definitions.append(self.buildDefinition(definition))
        return property_definitions

    def newCustomProperty(self, ref, property_definition, saveComment):
        if isinstance(property_definition, PropertyDefinition):
            property_definition = json.loads(property_definition.to_json())
        url = "{0}{1}/PropertyDefinitions".format(self.baseurl, ref)
        payload = {
            'saveComment': saveComment,
            'propertyDefinition': property_definition
        }
        return self.post(url, payload)

    def updatePropertyDefinitions(self, ref,
                                  property_name,
                                  property_definition,
                                  updateExisting,
                                  saveComment):
        if isinstance(property_definition, PropertyDefinition):
            property_definition = json.loads(property_definition.to_json())
        payload = {
            'updateExisting': updateExisting,
            'saveComment': saveComment,
            'propertyDefinition': property_definition
        }
        return self.put("{0}{1}/PropertyDefinitions/{2}".format(self.baseurl,
                                                                ref,
                                                                property_name),
                        payload)

    def deletePropertyDefinition(self, ref, property_name, saveComment):
        query_string = ""
        if saveComment:
            query_string = "?{0}".format(saveComment)
        return self.delete("{0}{1}/PropertyDefinitions/{2}{3}".format(self.baseurl,
                                                                      ref,
                                                                      property_name,
                                                                      query_string))
