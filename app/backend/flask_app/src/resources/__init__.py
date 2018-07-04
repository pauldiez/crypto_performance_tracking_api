class ResponseDataBuilder():
    """ This is the core crypto feed ResponseDataBuilder.
    It handles setting the data result sets, processing totals and metadata.
    """
    metadata = {}
    data = {}
    totals = {}
    response = {}

    def __init__(self, results=None, process_totals=True):

        # if results are passed in wrap data into a list if not already
        if results:
            if type(results) is not list:
                results = [results]

            # set metadata nad data variables
            self.set_metadata(self.process_metadata(results))
            self.set_data(results)

            if process_totals:

                # set and process totals
                self.set_totals(self.process_totals(results))

    def get_response(self):

        # build response structure and return
        self.response = {
            "metadata": self.get_metadata(),
            "data": self.get_data(),
            "totals": self.get_totals(),
        }
        return self.response

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    @staticmethod
    def process_metadata(results):
        # calculate total number of records
        metadata = {"total_records": len(results)}
        return metadata

    def set_metadata(self, metadata):
        self.metadata = metadata

    def get_metadata(self):
        return self.metadata

    @staticmethod
    def process_totals(results):
        totals = {}

        # loop through data result set and process the totals
        for result in results:

            # check if totals already exist
            if "totals" in result:

                # set total fields to zero
                if not totals:
                    for total_field, total_value in result['totals'].items():
                        totals[total_field] = 0

                # loop through each records of totals and globally sum up all totals
                for total_field, total_value in result['totals'].items():
                    totals[total_field] += total_value

        return totals

    def set_totals(self, totals):
        self.totals = totals

    def get_totals(self):
        return self.totals
