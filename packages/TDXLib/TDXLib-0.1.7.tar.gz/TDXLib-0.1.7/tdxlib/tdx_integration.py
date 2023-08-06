import configparser
import requests
import json
import getpass
import tdxlib.tdx_api_exceptions


class TDXIntegration:

    # Hard-coded into TDX
    component_ids = {
        'account': 14,
        'asset': 27,
        'configuration_item': 63,
        'contract': 29,
        'file_cabinet': 8,
        'issue': 3,
        'opportunity': 11,
        'person': 31,
        'product': 37,
        'product_model': 30,
        'project': 1,
        'ticket': 9,
        'vendor': 28
    }

    def __init__(self, filename=None):
        self.settings = None
        self.api_url = None
        self.username = None
        self.password = None
        self.token = None
        self.config = configparser.ConfigParser()

        # Read in configuration
        if filename is not None:
            self.config.read(filename)
        else:
            filename = 'tdxlib.ini'
            self.config.read(filename)
        if 'TDX API Settings' not in self.config:
            self.config['TDX API Settings'] = {
                'orgname': 'myuniversity',
                'sandbox': True,
                'username': '',
                'password': 'Prompt',
                'ticketAppId': '',
                'assetAppId': '',
                'caching': False
            }

            # Initialization wizard
            print("\nNo configuration file found. Please enter the following information: ")
            print("\n\nPlease enter your TeamDynamix organization name.")
            print("This is the teamdynamix.com subdomain that you use to access TeamDynamix.")
            init_orgname = input("Organization Name (<orgname>.teamdynamix.com): ")
            self.config.set('TDX API Settings', 'orgname', init_orgname)
            sandbox_invalid = True
            while sandbox_invalid:
                sandbox_choice = input("\nUse TeamDynamix Sandbox? [Y/N]: ")
                if sandbox_choice.lower() in ['y', 'ye', 'yes', 'true']:
                    self.config.set('TDX API Settings', 'sandbox', 'true')
                    sandbox_invalid = False
                elif sandbox_choice.lower() in ['n', 'no', 'false']:
                    self.config.set('TDX API Settings', 'sandbox', 'false')
                    sandbox_invalid = False
            init_username = input("\nTDX API Username (tdxuser@orgname.com): ")
            self.config.set('TDX API Settings', 'username', init_username)
            print("\nTDXLib can store the password for the API user in the configuration file.")
            print("This is convenient, but not very secure.")
            password_invalid = True
            while password_invalid:
                password_choice = input("Store password for " + init_username + "? [Y/N]: ")
                if password_choice.lower() in ['y', 'ye', 'yes', 'true']:
                    password_prompt = '\nEnter Password for ' + init_username + ": "
                    init_password = getpass.getpass(password_prompt)
                    self.config.set('TDX API Settings', 'password', init_password)
                    password_invalid = False
                elif password_choice.lower() in ['n', 'no', 'false']:
                    self.config.set('TDX API Settings', 'password', 'Prompt')
                    password_invalid = False
                if password_invalid:
                    print("Invalid Response.")
            init_ticket_id = input("\nTickets App ID (optional): ")
            self.config.set('TDX API Settings', 'ticketAppId', init_ticket_id)
            init_asset_id = input("\nAssets App ID (optional): ")
            self.config.set('TDX API Settings', 'assetAppId', init_asset_id)
            print("\nTDXLib uses intelligent caching to speed up API calls on repetitive operations.")
            print("In very dynamic environments, TDXLib's caching can cause issues.")
            caching_invalid = True
            while caching_invalid:
                caching_choice = input("Disable Caching? [Y/N]: ")
                if caching_choice.lower() in ['y', 'ye', 'yes', 'true']:
                    self.config.set('TDX API Settings', 'caching', 'true')
                    self.caching = False
                    caching_invalid = False
                elif caching_choice.lower() in ['n', 'no', 'false']:
                    self.config.set('TDX API Settings', 'caching', 'false')
                    self.caching = True
                    caching_invalid = False
                if caching_invalid:
                    print("Invalid Response.")
            print('\n\nInitial settings saved to: ' + filename)
            with open(filename, 'w') as configfile:
                self.config.write(configfile)

        # Read settings in
        self.settings = self.config['TDX API Settings']
        self.org_name = self.settings.get('orgname')
        self.sandbox = bool(self.settings.get('sandbox'))
        self.username = self.settings.get('username')
        self.password = self.settings.get('password')
        self.ticket_app_id = self.settings.get('ticketAppId')
        self.asset_app_id = self.settings.get('assetAppId')
        self.caching = bool(self.settings.get('caching'))
        if self.sandbox:
            api_end = '/SBTDWebApi/api'
        else:
            api_end = '/TDWebApi/api'
        self.api_url = 'https://' + self.org_name + '.teamdynamix.com' + api_end
        if self.password == 'Prompt':
            pass_prompt = 'Enter the TDX Password for user ' + self.username + '(this password will not be stored): '
            self.password = getpass.getpass(pass_prompt)
        try:
            response = requests.post(
                url=str(self.api_url) + '/auth',
                headers={
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps({
                    "username": self.username,
                    "password": self.password
                })
            )
            if response.status_code != 200:
                raise tdxlib.tdx_api_exceptions.TdxApiHTTPError(" Response code: " + str(response.status_code) + " " +
                                                                response.reason + "\n" + " Returned: " + response.text)
            else:
                self.token = response.text
                self.password = None
        except requests.exceptions.RequestException:
            print('HTTP Request failed')
        except tdxlib.tdx_api_exceptions.TdxApiHTTPError as e:
            print('Authorization failed.\n' + str(e))
        self.cache = {}
        self.clean_cache()

    def make_get(self, request_url):
        """
        Makes a HTTP GET request to the TDX Api.

        :param request_url: the path (everything after /TDWebAPI/api/) to call

        :return: the API response

        """
        get_url = self.api_url + request_url
        response = None
        try:
            response = requests.get(
                url=get_url,
                headers={
                    "Authorization": 'Bearer ' + self.token,
                    "Content-Type": "application/json; charset=utf-8",
                }
            )
            if response.status_code != 200:
                raise tdxlib.tdx_api_exceptions.TdxApiHTTPError(" Response code: " + str(response.status_code) + " " +
                                                                response.reason + "\n" + " Returned: " + response.text)
            val = response.json()
            return val
        except requests.exceptions.RequestException:
            print('HTTP Request failed')
        except tdxlib.tdx_api_exceptions.TdxApiHTTPError as e:
            print('GET failed: to ' + get_url + "\nReturned: " + str(e))
        except json.decoder.JSONDecodeError:
            message = 'Invalid JSON received from ' + get_url + ':'
            if response:
                message += response.text
            print(message)

    def make_post(self, request_url, body):
        """
        Makes a HTTP POST request to the TDX Api

        :param request_url: the path (everything after /TDWebAPI/api/) to call
        :param body: dumped JSON data to send with the POST

        :return: the API response

        """
        post_url = self.api_url + request_url
        response = None
        try:
            response = requests.post(
                url=post_url,
                headers={
                    "Authorization": 'Bearer ' + self.token,
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps(body))
            if response.status_code not in [200, 201]:
                raise tdxlib.tdx_api_exceptions.TdxApiHTTPError(
                    " Response code: " + str(response.status_code) + " " +
                    response.reason + "\n" + "Returned: " + response.text)
            val = response.json()
            return val
        except requests.exceptions.RequestException:
            print('HTTP Request failed')
        except tdxlib.tdx_api_exceptions.TdxApiHTTPError as e:
            print('POST failed: to ' + post_url + "\nReturned: " + str(e))
        except json.decoder.JSONDecodeError:
            message = 'Invalid JSON received from ' + post_url + ':\n'
            if response:
                message += response.text
            print(message)

    def make_put(self, request_url, body):
        """
        Makes an HTTP PUT request to the TDX API.

        :param request_url: the path (everything after /TDWebAPI/api/) to call
        :param body: dumped JSON data to send with the PUT

        :return: the API response

        """
        put_url = self.api_url + request_url
        response = None
        try:
            response = requests.put(
                url=put_url,
                headers={
                    "Authorization": 'Bearer ' + self.token,
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps(body))
            if response.status_code not in [200, 202, 204]:
                raise tdxlib.tdx_api_exceptions.TdxApiHTTPError(
                    " Response code: " + str(response.status_code) + " " +
                    response.reason + "\n" + "Returned: " + response.text)
            val = response.json()
            return val
        except requests.exceptions.RequestException:
            print('HTTP Request failed')
        except tdxlib.tdx_api_exceptions.TdxApiHTTPError as e:
            print('PUT failed: to ' + put_url + "\nReturned: " + str(e))
        except json.decoder.JSONDecodeError:
            message = 'Invalid JSON received from ' + put_url + ':\n'
            if response:
                message += response.text
            print(message)

    def make_delete(self, request_url):
        """
        Makes an HTTP DELETE request to the TDX Api.

        :param request_url: the path (everything after /TDWebAPI/api/) to call

        :return: the API's response

        """
        delete_url = self.api_url + request_url
        response = None
        try:
            response = requests.delete(
                url=delete_url,
                headers={
                    "Authorization": 'Bearer ' + self.token,
                    "Content-Type": "application/json; charset=utf-8",
                })
            if response.status_code not in [200, 201]:
                raise tdxlib.tdx_api_exceptions.TdxApiHTTPError(
                    " Response code: " + str(response.status_code) + " " +
                    response.reason + "\n" + "Returned: " + response.text)
            val = response.json()
            return val
        except requests.exceptions.RequestException:
            print('HTTP DELETE Request failed')
        except tdxlib.tdx_api_exceptions.TdxApiHTTPError as e:
            print('DELETE failed: to ' + delete_url + "\nReturned: " + str(e))
        except json.decoder.JSONDecodeError:
            message = 'Invalid JSON received from ' + delete_url + ':\n'
            if response:
                message += response.text
            print(message)

    def make_patch(self, request_url, body: list):
        """
        Makes an HTTP PATH request to the TDX Api.

        The TeamDyanmix API supports limited PATCH functionality. Since TDX data is highly structured, items are
        referenced explicitly by their TDX ID, and not by their order in the object. Likewise, since the fields
        in a TDX object are all predefined, a PATCH call cannot add or remove any fields in the object.

        :param request_url: the path (everything after /TDWebAPI/api/) to call
        :param body: a list of PATCH operations as dictionaries, each including the keys "op", "path", and "value"

        :return: the API's response

        """
        patch_url = self.api_url + request_url
        response = None
        try:
            response = requests.patch(
                url=patch_url,
                headers={
                    "Authorization": 'Bearer ' + self.token,
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps(body)
            )

            if response.status_code not in [200, 201]:
                raise tdxlib.tdx_api_exceptions.TdxApiHTTPError(
                    " Response code: " + str(response.status_code) + " " +
                    response.reason + "\n" + "Returned: " + response.text)
            val = response.json()
            return val
        except requests.exceptions.RequestException:
            print('HTTP PATCH Request failed')
        except tdxlib.tdx_api_exceptions.TdxApiHTTPError as e:
            print('PATCH failed: to ' + patch_url + "\nReturned: " + str(e))
        except json.decoder.JSONDecodeError:
            message = 'Invalid JSON received from ' + patch_url + ':\n'
            if response:
                message += response.text
            print(message)

    def clean_cache(self):
        self.cache = {
            'locations': {},
            'rooms': {},
            'people': {},
            'groups': {},
            'accounts': {},
            'custom_attributes': {}
        }

    # #### GETTING TDX OBJECTS #### #

    def get_tdx_item_by_id(self, obj_type, key):
        """
        A generic function to get something from the TDX API using its ID/UID.

        Since the TDX API endpoints are almost all in the form /<object type>/id, this method gives an easy way
        to template all the different get_<object>_by_id methods.

        :param obj_type: the type of object to get.
        :param key: the ID number of an object to get, as a string

        :return: list of person data
        """
        url_string = f'/{obj_type}/{key}'
        return self.make_get(url_string)

    def get_location_by_id(self, location_id):
        """
        Gets a group by the group ID.

        :param location_id: ID number of group to get members of

        :return: list of person data
        """
        return self.get_tdx_item_by_id('locations', location_id)

    def get_account_by_id(self, account_id):
        """
        Gets an account by the account ID.

        :param account_id: ID number of group to get members of

        :return: list of person data
        """
        return self.get_tdx_item_by_id('accounts', account_id)

    def get_group_by_id(self, group_id):
        """
        Gets a group by the group ID.

        :param group_id: ID number of group to get members of

        :return: list of person data
        """
        return self.get_tdx_item_by_id('groups', group_id)

    def get_person_by_uid(self, uid):
        """
        Gets a a person by UID.

        :param uid: uid string of a person

        :return: dict of person data
        """
        return self.get_tdx_item_by_id('people', uid)

    def get_group_members_by_id(self, group_id):
        """
        Gets a list of group members by the group ID.

        :param group_id: ID number of group to get members of

        :return: list of person data
        """
        return self.get_tdx_item_by_id('groups', group_id + '/members')
    
    def search_people(self, key):
        """
        Gets the top match of people with search text, such as:
        - Name
        - Email
        - Username
        - Organizational ID

        :param key: string with search text of person to search with

        :return: dict of person data

        """
        if key in self.cache['people']:
            return self.cache['people'][key]
        else:
            url_string = "/people/lookup?searchText=" + str(key) + "&maxResults=1"
            people = self.make_get(url_string)
            if len(people) == 0:
                raise tdxlib.tdx_api_exceptions.TdxApiObjectNotFoundError("No person found for " + key)
            self.cache['people'][key] = people[0]
            return people[0]

    def get_all_accounts(self):
        """
        Gets all accounts

        :return: list of Account data in json format

        """
        url_string = "/accounts"
        return self.make_get(url_string)

    def get_account_by_name(self, key, additional_params=None):
        """
        Gets an account with name key.
        
        :param key: name of an account to search for
        :param additional_params: other search items, as a dict, as described in TDX Api Docs
        
        :return: dict of account data (not complete, but including the ID)

        """
        if key in self.cache['accounts']:
            return self.cache['accounts'][key]
        else:
            url_string = '/accounts/search'
            search_params = {'SearchText': key, 'IsActive': True, 'MaxResults': 5}
            if additional_params:
                search_params.update(additional_params)
            post_body = dict({'search': search_params})
            accounts = self.make_post(url_string, post_body)
            for account in accounts:
                if key.lower() in account['Name'].lower():
                    self.cache['accounts'][key] = account
                    return account
            raise tdxlib.tdx_api_exceptions.TdxApiObjectNotFoundError('No account found for ' + key)

    def get_all_groups(self):
        """
        Gets a list of groups

        :return: list of group data as dicts

        """
        url_string = "/groups/search"
        post_body = {'search': {'NameLike': "", 'IsActive': 'True'}}
        return self.make_post(url_string, post_body)

    def get_group_by_name(self, key, additional_params=None):
        """
        Gets a group with name key.

        :param key: name of Group to search for
        :param additional_params: other search items, as a dict, as described in TDX Api Docs

        :return: a dict of group data (not complete, but including the ID)

        """
        if key in self.cache['groups']:
            return self.cache['groups'][key]
        else:
            url_string = '/groups/search'
            search_params = {'NameLike': key, 'IsActive': True}
            if additional_params:
                search_params.update(additional_params)
            post_body = dict({'search': search_params})
            groups = self.make_post(url_string, post_body)
            if type(groups) is not list:
                if key.lower() in groups['Name'].lower():
                    self.cache['groups'][key] = groups
                    return groups
            else:
                for group in groups:
                    if key.lower() in group['Name'].lower():
                        self.cache['groups'][key] = group
                        return group
            raise tdxlib.tdx_api_exceptions.TdxApiObjectNotFoundError('No group found for ' + key)

    def get_all_group_members(self, key):
        """
        Gets all the members of a group as person objects.

        :param key: a partial name

        :return: list of groups

        """

    def get_all_custom_attributes(self, object_type, associated_type=0, app_id=0):
        """
        Gets all custom attributes for the component type. 
        See https://solutions.teamdynamix.com/TDClient/KB/ArticleDet?ID=22203 for possible values.

        :param associated_type: the associated type of object to get attributes for, default: 0
        :param app_id: the application number to get attributes from, default: 0
        :param object_type: the object type to get attributes for (tickets = 9, assets = 27, CI's = 63)

        :return: dictionary of custom attributes with options

        """
        url_string = '/attributes/custom?componentId=' + str(object_type) + '&associatedTypeId=' + \
            str(associated_type) + '&appId=' + str(app_id)
        return self.make_get(url_string)

    def get_custom_attribute_by_name(self, key, object_type):
        """
        Gets a custom attribute for the component type.
        See https://solutions.teamdynamix.com/TDClient/KB/ArticleDet?ID=22203 for possible values.

        :param key: the name of the custom attribute to search for
        :param object_type: the object type to get attributes for (tickets = 9, assets = 27, CI's = 63)

        :return: the attribute as a dict, with all choice items included

        """
        if not self.cache['custom_attributes'][str(object_type)]:
            # There is no API for searching attributes -- the only way is to get them all.
            self.cache['custom_attributes'][str(object_type)] = self.get_all_custom_attributes(object_type)
        for item in self.cache['custom_attributes'][str(object_type)]:
            if key.lower() in item['Name'].lower():
                self.cache['custom_attributes'][str(object_type)][key] = item
                return item
        raise tdxlib.tdx_api_exceptions.TdxApiObjectNotFoundError(
            "No custom attribute found for " + key + ' and object type ' + str(object_type))

    @staticmethod
    def get_custom_attribute_value_by_name(attribute, key):
        """
        Gets the choice item from a custom attribute for the component type.
        See https://solutions.teamdynamix.com/TDClient/KB/ArticleDet?ID=22203 for possible values.

        :param key: the name of the choice to look for
        :param attribute: the attribute (as retrieved from get_attribute_by_name())

        :return: the the choice object from this attribute whose name matches the key

        """
        for i in attribute['Choices']:
            if key.lower() in i['Name'].lower():
                return i
        raise tdxlib.tdx_api_exceptions.TdxApiObjectNotFoundError(
            "No custom attribute value for " + key + " found in " + attribute['Name'])

    def get_all_locations(self):
        url_string = '/locations'
        return self.make_get(url_string)

    def get_location_by_name(self, key, additional_params=None):
        """
        Gets a location with name key.

        :param key: name of location to search for
        :param additional_params: other search items, as a dict, as described in TDX Api Docs

        :return: a dict of location data

        """
        if key in self.cache['locations']:
            return self.cache['locations'][key]
        else:
            url_string = '/locations/search'
            search_params = {'NameLike': key, 'IsActive': True}
            if additional_params:
                search_params.update(additional_params)
            post_body = dict({'search': search_params})
            locations = self.make_post(url_string, post_body)
            for location in locations:
                if key.lower() in location['Name'].lower():
                    full_location = self.get_location_by_id(location['ID'])
                    self.cache['locations'][key] = full_location
                    return full_location
            raise tdxlib.tdx_api_exceptions.TdxApiObjectNotFoundError("No location found for " + key)

    @staticmethod
    def get_room_by_name(location, room):
        """
        Gets a room by its name.

        :param location: dict of location info from get_location_by_name()
        :param room: name of a room to search for (must be exact)

        :return: a dict with all the the information regarding the room. Use this to retrieve the ID attribute.

        """
        for i in location['Rooms']:
            if room.lower in i['Name'].lower():
                return i
        raise tdxlib.tdx_api_exceptions.TdxApiObjectNotFoundError(
            "No room found for " + room + " in location " + location['Name'])

    # #### CREATING TDX OBJECTS #### #

    # #### #### ACCOUNTS #### #### #
    # https://api.teamdynamix.com/TDWebApi/Home/section/Accounts

    def create_account(self, name: str, is_active: bool, manager: str, additional_info: dict,
                       custom_attributes: dict) -> dict:
        """
        Creates an account in TeamDynamix

        :param name: Name of account to create.
        :param manager: email address of the TDX Person who will be the manager of the group
        :param additional_info: dict of other attributes to set on account. Retrieved from:
                                https://api.teamdynamix.com/TDWebApi/Home/type/TeamDynamix.Api.Accounts.Account
        :param custom_attributes: dict of names of custom attributes and corresponding names of the choices to set
                                  on each attribute. These names must match the names in TDX exactly.

        :return: a dict with information about the created account

        """
        editable_account_attributes = ['Address1', 'Address2', 'Address3', 'Address4', 'City', 'StateAbbr',
                                       'PostalCode', 'Country', 'Phone', 'Fax', 'Url', 'Notes', 'Code', 'IndustryID']
        url_string = '/accounts'
        # Set up data for account
        data = dict()
        data['Name'] = name
        data['ManagerUID'] = self.search_people(manager)['UID']
        for attrib, value in additional_info:
            if attrib in editable_account_attributes:
                data[attrib] = additional_info[attrib]
        for attrib, value in custom_attributes:
            tdx_attrib = self.get_custom_attribute_by_name(attrib, TDXIntegration.component_ids['account'])
            tdx_attrib_value = self.get_custom_attribute_value_by_name(tdx_attrib, value)
            data['Attributes'][tdx_attrib['ID']] = tdx_attrib_value['ID']
        post_body = dict({'account': data})
        return self.make_post(url_string, post_body)

    # TODO: def edit_account()
    #   https://api.teamdynamix.com/TDWebApi/Home/type/TeamDynamix.Api.Accounts.Account

    # #### #### GROUPS #### #### #
    # https://api.teamdynamix.com/TDWebApi/Home/section/Group

    # TODO: def create_group()

    # TODO: def edit_group()
    #    https://api.teamdynamix.com/TDWebApi/Home/type/TeamDynamix.Api.Users.Group

    # TODO: def delete_group()

    # TODO: def set_group_members()
    #  This should ingest a list of people. We need to decide whether or not it should be a list of email
    #  addresses, or a list of UUID's that could be generated from another method.

    # #### PEOPLE #### #
    # https://api.teamdynamix.com/TDWebApi/Home/section/People #summary

    # TODO: def create_person()

    # TODO: def edit_person()

    # TODO: def get_person_functional_roles() -- accept UUID or email

    # TODO: def delete_person_functional_role() -- accept UUID or email

    # TODO: def add_person_functional_role() -- accept UUID or email

    # TODO: def get_groups_by_person() -- accept UUID or email

    # TODO: def remove_user_from_group() -- accept UUID or email

    # TODO: def add_person_to_groups() -- accept single or multiple groups, support removal from all other groups

    # TODO: def set_person_status() -- enable/disable

    # TODO: def person_import() -- this could be difficult -- have to figure out how to upload an xlsx file via API.

    # #### #### LOCATIONS & ROOMS #### #### #
    # https://api.teamdynamix.com/TDWebApi/Home/section/Locations

    # TODO: create_location()

    # TODO: edit_location()

    # TODO: create_room()

    # TODO: delete_room()

    # TODO: edit_room()

    # #### #### ATTRIBUTE CHOICES #### #### #
    # https: // api.teamdynamix.com / TDWebApi / Home / section / Attributes

    # TODO: add_custom_attribute_choice()

    # TODO: delete_custom_attribute_choice()

    # TODO: edit_custom_attribute_choice():
