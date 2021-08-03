from ajax_select import register, LookupChannel
from .models import JobTitles
from hourglass.references.models import CompanyRef


@register('titles')
class JobTitlesLookup(LookupChannel):
    model = JobTitles

    def get_query(self, q, request):
          return self.model.objects.filter(name__icontains=q).order_by('name')


@register('titles_campaign')
class JobTitlesLookupCampaign(LookupChannel):
    model = JobTitles

    def get_query(self, q, request):
          return self.model.objects.filter(name__icontains=q).order_by('name')



@register('company_ref')
class JobTitlesLookupCampaign(LookupChannel):
    model = CompanyRef

    def get_query(self, q, request):
          return self.model.objects.filter(name__icontains=q).order_by('name')