import routeros_api
from config import MIKROTIK_ROUTER

class MikrotikAPI:
    def __init__(self):
        self.connection = routeros_api.RouterOsApiPool(
            host=MIKROTIK_ROUTER['host'],
            username=MIKROTIK_ROUTER['username'],
            password=MIKROTIK_ROUTER['password'],
            port=MIKROTIK_ROUTER['port'],
            plaintext_login=True
        )
        self.api = self.connection.get_api()

    def disconnect(self):
        self.connection.disconnect()

    def add_pppoe_user(self, username, password, local_address=None, remote_address=None):
        secrets = self.api.get_resource('/ppp/secret')

        data = {
            'name': username,
            'password': password,
            'service': 'pppoe'
        }

        if local_address:
            data['local-address'] = local_address
        if remote_address:
            data['remote-address'] = remote_address

        secrets.add(**data)

    def delete_pppoe_user(self, username):
        secrets = self.api.get_resource('/ppp/secret')
        user = secrets.get(name=username)

        # Kalau user gak ada, anggap udah dihapus biar gak keluar error
        if not user:
            return True

        user_id = user[0].get('.id') or user[0].get('id')

        if user_id:
            secrets.remove(id=user_id)

        return True

    def get_pppoe_users(self):
        secrets = self.api.get_resource('/ppp/secret')
        return secrets.get()

    def get_pppoe_user(self, username):
        secrets = self.api.get_resource('/ppp/secret')
        user = secrets.get(name=username)
        if user:
            return user[0]
        return None


#------------------------------------- dibawah script tambah ip address --------------------------------------------#

    def add_ip_address(self, address, network, interface):
        ip_resource = self.api.get_resource('/ip/address')
        ip_resource.add(address=address, network=network, interface=interface)

    def delete_ip_address(self, address):
        ip_resource = self.api.get_resource('/ip/address')
        ip_item = ip_resource.get(address=address)

        if not ip_item:
            raise Exception(f"IP Address '{address}' tidak ditemukan.")

        # Ambil ID (prioritas 'id' dulu, baru fallback ke '.id')
        ip_id = ip_item[0].get('id') or ip_item[0].get('.id')

        if not ip_id:
            raise Exception(f"IP Address '{address}' ditemukan, tapi tidak memiliki ID.")

        ip_resource.remove(id=ip_id)

 # -------------------- Firewall Rule Management --------------------
    def add_firewall_rule(self, table, chain, action, src_address, dst_address, protocol, port):
        firewall = self.api.get_resource(f'/ip/firewall/{table}')

        data = {
            'chain': chain,
            'action': action,
            'src-address': src_address,
            'dst-address': dst_address,
            'protocol': protocol,
            'port': port
        }

        firewall.add(**data)


    def delete_firewall_rule(self, table, rule_id):
        firewall = self.api.get_resource(f'/ip/firewall/{table}')
        firewall.remove(id=rule_id)

    def get_firewall_rules(self, table, chain=None):
        firewall = self.api.get_resource(f'/ip/firewall/{table}')
        if chain:
            return firewall.get(chain=chain)
        return firewall.get()
