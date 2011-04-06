"""
   Copyright 2011 Sami Dalouche

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from genshi.template import NewTextTemplate, MarkupTemplate
class OutputFile(object):
    def __init__(self, profile_provider, target_path, template_path, template_format):
        assert profile_provider is not None, "profile_provider is required"
        assert target_path is not None, "target_path is required"
        assert template_path is not None, "template_path is required"
        assert template_format is not None, "template_format is required"
        self._profile_provider = profile_provider
        self._target_path = target_path
        self._template_path = template_path
        (self._template_engine,self._template_format)  = template_format.split('-')
        assert self._template_engine == 'genshi', "genshi is the only supported template engine. Not recognized: %s" % (self._template_engine,)
        assert self._template_format in ['text', 'xhtml', 'html', 'xml'], "Supported formats are: text, xhtml, html, xml"
    
    def with_profile(self, profile):
        return OutputFile(lambda: profile, 
                          self._target_path, 
                          self._template_path, 
                          self._template_engine + "-" + self._template_format)

    def render(self, template_loader):
        stream = template_loader.load(self._template_path, cls=self._markup_template()).generate(**self._profile_provider().properties)
        return stream.render(self._template_format).strip()
            
        
    def get_target_path(self):
        tmpl = NewTextTemplate(self._target_path)
        stream = tmpl.generate(**self._profile_provider().properties)
        return stream.render('text').strip()
    
    def _markup_template(self):
        def text():
            return NewTextTemplate
        def markup():
            return MarkupTemplate
        strategy = None
        if(self._template_format == 'text'):
            strategy = text
        else:
            strategy = markup
        return strategy
            
    target_path = property(get_target_path, None)