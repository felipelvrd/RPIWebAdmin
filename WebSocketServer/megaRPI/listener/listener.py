
from mega import MegaListener, MegaError, MegaRequest


class AppListener(MegaListener):
    def __init__(self):
        super(AppListener, self).__init__()
        self.cwd =None

    def onRequestStart(self, api, request):
        print('Request start ({})'.format(request))


    def onRequestFinish(self, api, request, error):
        print('Request finished ({}); Result: {}'
                     .format(request, error))
        if error.getErrorCode() != MegaError.API_OK:
            return

        request_type = request.getType()
        if request_type == MegaRequest.TYPE_LOGIN:
            api.fetchNodes()
            print 'hola login'
        elif request_type == MegaRequest.TYPE_EXPORT:
            print('Exported link: {}'.format(request.getLink()))
        elif request_type == MegaRequest.TYPE_ACCOUNT_DETAILS:
            account_details = request.getMegaAccountDetails()
            print('Account details received')
            print('Account e-mail: {}'.format(api.getMyEmail()))
            print('Storage: {} of {} ({} %)'
                         .format(account_details.getStorageUsed(),
                                 account_details.getStorageMax(),
                                 100 * account_details.getStorageUsed()
                                 / account_details.getStorageMax()))
            print('Pro level: {}'.format(account_details.getProLevel()))


    def onRequestTemporaryError(self, api, request, error):
        print('Request temporary error ({}); Error: {}'
                .format(request, error))


    def onTransferFinish(self, api, transfer, error):
        print('Transfer finished ({}); Result: {}'
                .format(transfer, transfer.getFileName(), error))


    def onTransferUpdate(self, api, transfer):
        print('Transfer update ({} {});'
                     ' Progress: {} KB of {} KB, {} KB/s'
                     .format(transfer,
                             transfer.getFileName(),
                             transfer.getTransferredBytes() / 1024,
                             transfer.getTotalBytes() / 1024,
                             transfer.getSpeed() / 1024))


    def onTransferTemporaryError(self, api, transfer, error):
        print('Transfer temporary error ({} {}); Error: {}'
                     .format(transfer, transfer.getFileName(), error))


    def onUsersUpdate(self, api, users):
        if users != None:
            print('Users updated ({})'.format(users.size()))

    def onNodesUpdate(self, api, nodes):
        if nodes != None:
            print('Nodes updated ({})'.format(nodes.size()))
        else:
            self.cwd = api.getRootNode()
