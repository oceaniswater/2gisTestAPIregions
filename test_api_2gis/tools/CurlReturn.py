class CurlReturn:
    @staticmethod
    def curlReturn(result):
        command = "curl --location --request {method} '{uri}' --header {headers} --data-raw '{data}'"
        method = result.request.method
        uri = result.request.url
        data = result.request.body
        headers = ["'{0}: {1}'".format(k, v) for k, v in result.request.headers.items()]
        headers = " --header ".join(headers)

        if data is not None:
            return command.format(method=method,
                                  headers=headers,
                                  data=data,
                                  uri=uri)
        else:
            command = "curl --location --request {method} '{uri}' --header {headers}"
            return command.format(method=method,
                                  headers=headers,
                                  uri=uri)
