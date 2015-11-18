from django import template

register = template.Library()

@register.tag
def switch(parser, token):
    """
    Switch tag. Usage::

      {% switch meal %}
        {% case "spam" %}...{% endcase %}
        {% case "eggs" %}...{% endcase %}
        {% default %}
          No case matched.
        {% enddefault %}
      {% endswitch %}

    Note that ``{% case %}`` arguments can be variables if you like (as can
    switch arguments, buts that's a bit silly).

    The default case is optional. If you wish to fail if nothing matched, you
    can use::

      {% switch meal %}
        {% case "spam" %}...{% endcase %}
        {% case "eggs" %}...{% endcase %}
        {% default %}
          {% error %}
        {% enddefault %}
      {% endswitch %}

    """

    # Parse out the arguments.
    args = token.split_contents()

    if len(args) != 2:
        raise template.TemplateSyntaxError(
            "%s tag takes exactly 1 argument." % args[0]
        )

    # Pull out all the children of the switch tag (until {% endswitch %}).
    childnodes = parser.parse(('endswitch', 'default'))

    token = parser.next_token()
    default = template.NodeList()

    if token.contents == 'default':
        default = parser.parse(('enddefault',))
        parser.delete_first_token()
        parser.parse(('endswitch',))
        parser.delete_first_token()

    # We just care about case children; all other direct children get ignored.
    casenodes = childnodes.get_nodes_by_type(CaseNode)

    return SwitchNode(parser.compile_filter(args[1]), casenodes, default)

@register.tag
def case(parser, token):
    args = token.split_contents()

    # Same dance as above, except this time we care about all the child nodes
    children = parser.parse(('endcase',))

    parser.delete_first_token()

    return CaseNode(
        [parser.compile_filter(x) for x in args[1:]],
        children,
    )

class SwitchNode(template.Node):
    def __init__(self, value, cases, default):
        self.value = value
        self.cases = cases
        self.default = default

    def render(self, context):
        value = self.value.resolve(context)

        # Check each case, and if it matches return the rendered content
        # of that case (short-circuit).
        for case in self.cases:
            if case.equals(value, context):
                return case.render(context)

        # No matches; render the default
        return self.default.render(context)

class CaseNode(template.Node):
    def __init__(self, values, childnodes):
        self.values = values
        self.childnodes = childnodes

    def equals(self, otherval, context):
        """
        Check to see if any of this case's values equals some other value. This
        is called from ``SwitchNode.render()``, above.
        """

        for value in self.values:
            if value.resolve(context) == otherval:
                return True

        return False

    def render(self, context):
        """
        Render this particular case, which means rendering its child nodes.
        """

        return self.childnodes.render(context)
