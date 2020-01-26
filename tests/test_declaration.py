from unittest import TestCase

from colosseum import engine as css_engine
from colosseum.colors import GOLDENROD, NAMED_COLOR, REBECCAPURPLE
from colosseum.constants import (
    AUTO, BLOCK, INHERIT, INITIAL, INLINE, LEFT, REVERT, RIGHT, RTL, TABLE,
    UNSET, Choices, OtherProperty,
)
from colosseum.declaration import CSS, validated_property
from colosseum.units import percent, px
from colosseum.validators import (
    is_color, is_integer, is_length, is_number, is_percentage,
)

from .utils import TestNode


class PropertyChoiceTests(TestCase):
    def test_none(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(None), initial=None)

        obj = MyObject()
        self.assertIsNone(obj.prop)

        with self.assertRaises(ValueError):
            obj.prop = 10
        with self.assertRaises(ValueError):
            obj.prop = 20 * px
        with self.assertRaises(ValueError):
            obj.prop = 30 * percent
        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE
        with self.assertRaises(ValueError):
            obj.prop = '#112233'
        with self.assertRaises(ValueError):
            obj.prop = 'a'
        with self.assertRaises(ValueError):
            obj.prop = 'b'
        obj.prop = None
        obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for CSS property 'prop'; Valid values are: none"
            )

    def test_allow_length(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(validators=[is_length]), initial=0)

        obj = MyObject()
        self.assertEqual(obj.prop, 0 * px)

        obj.prop = 10
        obj.prop = 20 * px
        obj.prop = 30 * percent
        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE
        with self.assertRaises(ValueError):
            obj.prop = '#112233'
        with self.assertRaises(ValueError):
            obj.prop = 'a'
        with self.assertRaises(ValueError):
            obj.prop = 'b'
        with self.assertRaises(ValueError):
            obj.prop = None
        with self.assertRaises(ValueError):
            obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for CSS property 'prop'; Valid values are: <length>"
            )

    def test_allow_percentage(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(validators=[is_percentage]), initial=99 * percent)

        obj = MyObject()
        self.assertEqual(obj.prop, 99 * percent)

        with self.assertRaises(ValueError):
            obj.prop = 10
        with self.assertRaises(ValueError):
            obj.prop = 20 * px
        obj.prop = 30 * percent
        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE
        with self.assertRaises(ValueError):
            obj.prop = '#112233'
        with self.assertRaises(ValueError):
            obj.prop = 'a'
        with self.assertRaises(ValueError):
            obj.prop = 'b'
        with self.assertRaises(ValueError):
            obj.prop = None
        with self.assertRaises(ValueError):
            obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for CSS property 'prop'; Valid values are: <percentage>"
            )

    def test_allow_integer(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(validators=[is_integer]), initial=0)

        obj = MyObject()
        self.assertEqual(obj.prop, 0)

        obj.prop = 10
        with self.assertRaises(ValueError):
            obj.prop = 20 * px
        with self.assertRaises(ValueError):
            obj.prop = 30 * percent
        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE
        with self.assertRaises(ValueError):
            obj.prop = '#112233'
        with self.assertRaises(ValueError):
            obj.prop = 'a'
        with self.assertRaises(ValueError):
            obj.prop = 'b'
        with self.assertRaises(ValueError):
            obj.prop = None
        with self.assertRaises(ValueError):
            obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for CSS property 'prop'; Valid values are: <integer>"
            )

    def test_allow_color(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(validators=[is_color]), initial='goldenrod')

        obj = MyObject()
        self.assertEqual(obj.prop, NAMED_COLOR[GOLDENROD])

        with self.assertRaises(ValueError):
            obj.prop = 10
        with self.assertRaises(ValueError):
            obj.prop = 20 * px
        with self.assertRaises(ValueError):
            obj.prop = 30 * percent
        obj.prop = REBECCAPURPLE
        obj.prop = '#112233'
        with self.assertRaises(ValueError):
            obj.prop = 'a'
        with self.assertRaises(ValueError):
            obj.prop = 'b'
        with self.assertRaises(ValueError):
            obj.prop = None
        with self.assertRaises(ValueError):
            obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for CSS property 'prop'; Valid values are: <color>"
            )

    def test_values(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices('a', 'b', None), initial='a')

        obj = MyObject()
        self.assertEqual(obj.prop, 'a')

        with self.assertRaises(ValueError):
            obj.prop = 10
        with self.assertRaises(ValueError):
            obj.prop = 20 * px
        with self.assertRaises(ValueError):
            obj.prop = 30 * percent
        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE
        with self.assertRaises(ValueError):
            obj.prop = '#112233'
        obj.prop = 'a'
        obj.prop = 'b'
        obj.prop = None
        obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for CSS property 'prop'; Valid values are: a, b, none"
            )

    def test_all_choices(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(
                'a', 'b', None,
                validators=[is_integer, is_number, is_length, is_percentage, is_color],
                explicit_defaulting_constants=[INITIAL, INHERIT, UNSET, REVERT]
            ), initial=None)

        obj = MyObject()

        obj.prop = 10
        obj.prop = 20 * px
        obj.prop = 30 * percent
        obj.prop = REBECCAPURPLE
        obj.prop = '#112233'
        obj.prop = 'a'
        obj.prop = 'b'
        obj.prop = None
        obj.prop = 'none'
        obj.prop = INITIAL
        obj.prop = INHERIT
        obj.prop = UNSET
        obj.prop = REVERT

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for CSS property 'prop'; "
                "Valid values are: <color>, <integer>, <length>, <number>, <percentage>, "
                "a, b, inherit, initial, none, revert, unset"
            )

    def test_string_symbol(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(AUTO, None), initial=None)

        obj = MyObject()

        # Set a symbolic value using the string value of the symbol
        # We can't just use the string directly, though - that would
        # get optimized by the compiler. So we create a string and
        # transform it into the value we want.
        val = 'AUTO'
        obj.prop = val.lower()

        # Both equality and instance checking should work.
        self.assertEqual(obj.prop, AUTO)
        self.assertIs(obj.prop, AUTO)


class CssDeclarationTests(TestCase):
    def test_engine(self):
        node = TestNode(style=CSS())
        self.assertEqual(node.style.engine(), css_engine)

    def test_auto_default_property(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        # Default value is AUTO
        self.assertIs(node.style.width, AUTO)
        self.assertIsNone(node.style.dirty)

        # Modify the value
        node.style.width = 10

        self.assertEqual(node.style.width, 10)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set the value to the same value.
        # Dirty flag is not set.
        node.style.width = 10
        self.assertEqual(node.style.width, 10)
        self.assertFalse(node.style.dirty)

        # Set the value to something new
        # Dirty flag is set.
        node.style.width = 20
        self.assertEqual(node.style.width, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property
        del node.style.width
        self.assertIs(node.style.width, AUTO)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property again.
        # The underlying attribute won't exist, so this
        # should be a no-op.
        del node.style.width
        self.assertIs(node.style.width, AUTO)
        self.assertFalse(node.style.dirty)

    def test_0_default_property(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        # Default value is 0
        self.assertEqual(node.style.border_top_width, 0)
        self.assertIsNone(node.style.dirty)

        # Modify the value
        node.style.border_top_width = 10

        self.assertEqual(node.style.border_top_width, 10)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set the value to the same value.
        # Dirty flag is not set.
        node.style.border_top_width = 10
        self.assertEqual(node.style.border_top_width, 10)
        self.assertFalse(node.style.dirty)

        # Set the value to something new
        # Dirty flag is set.
        node.style.border_top_width = 20
        self.assertEqual(node.style.border_top_width, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property
        del node.style.border_top_width
        self.assertEqual(node.style.border_top_width, 0)
        self.assertTrue(node.style.dirty)

    def test_None_default_property(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        # Default value is None
        self.assertIsNone(node.style.max_width)
        self.assertIsNone(node.style.dirty)

        # Modify the value
        node.style.max_width = 10

        self.assertEqual(node.style.max_width, 10)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set the value to the same value.
        # Dirty flag is not set.
        node.style.max_width = 10
        self.assertEqual(node.style.max_width, 10)
        self.assertFalse(node.style.dirty)

        # Set the value to something new
        # Dirty flag is set.
        node.style.max_width = 20
        self.assertEqual(node.style.max_width, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property
        del node.style.max_width
        self.assertIsNone(node.style.max_width)
        self.assertTrue(node.style.dirty)

    def test_property_with_choices(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        # Default value is INLINE
        self.assertIs(node.style.display, INLINE)
        self.assertIsNone(node.style.dirty)

        # Try to provide a value that isn't on the choices list
        with self.assertRaises(ValueError):
            node.style.display = 10

        # Use a valid value
        node.style.display = BLOCK
        self.assertIs(node.style.display, BLOCK)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set the value to the same value.
        # Dirty flag is not set.
        node.style.display = BLOCK
        self.assertIs(node.style.display, BLOCK)
        self.assertFalse(node.style.dirty)

        # Set the value to something new
        # Dirty flag is set.
        node.style.display = TABLE
        self.assertIs(node.style.display, TABLE)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property
        del node.style.display
        self.assertIs(node.style.display, INLINE)
        self.assertTrue(node.style.dirty)

    def test_directional_property(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        # Default value is 0
        self.assertEqual(node.style.margin, (0, 0, 0, 0))
        self.assertEqual(node.style.margin_top, 0)
        self.assertEqual(node.style.margin_right, 0)
        self.assertEqual(node.style.margin_bottom, 0)
        self.assertEqual(node.style.margin_left, 0)
        self.assertIsNone(node.style.dirty)

        # Set a value in one axis
        node.style.margin_top = 10

        self.assertEqual(node.style.margin, (10, 0, 0, 0))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 0)
        self.assertEqual(node.style.margin_bottom, 0)
        self.assertEqual(node.style.margin_left, 0)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a single item
        node.style.margin = (10,)

        self.assertEqual(node.style.margin, (10, 10, 10, 10))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 10)
        self.assertEqual(node.style.margin_bottom, 10)
        self.assertEqual(node.style.margin_left, 10)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a single item
        node.style.margin = 30

        self.assertEqual(node.style.margin, (30, 30, 30, 30))
        self.assertEqual(node.style.margin_top, 30)
        self.assertEqual(node.style.margin_right, 30)
        self.assertEqual(node.style.margin_bottom, 30)
        self.assertEqual(node.style.margin_left, 30)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a 2 values
        node.style.margin = (10, 20)

        self.assertEqual(node.style.margin, (10, 20, 10, 20))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 10)
        self.assertEqual(node.style.margin_left, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a 3 values
        node.style.margin = (10, 20, 30)

        self.assertEqual(node.style.margin, (10, 20, 30, 20))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 30)
        self.assertEqual(node.style.margin_left, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a 4 values
        node.style.margin = (10, 20, 30, 40)

        self.assertEqual(node.style.margin, (10, 20, 30, 40))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 30)
        self.assertEqual(node.style.margin_left, 40)
        self.assertTrue(node.style.dirty)

        # Set a value directly with an invalid number of values
        with self.assertRaises(ValueError):
            node.style.margin = ()

        with self.assertRaises(ValueError):
            node.style.margin = (10, 20, 30, 40, 50)

        # Clean the layout
        node.layout.dirty = False

        # Clear a value on one axis
        del node.style.margin_top

        self.assertEqual(node.style.margin, (0, 20, 30, 40))
        self.assertEqual(node.style.margin_top, 0)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 30)
        self.assertEqual(node.style.margin_left, 40)
        self.assertTrue(node.style.dirty)

        # Restore the top margin
        node.style.margin_top = 10

        # Clean the layout
        node.layout.dirty = False

        # Clear a value directly
        del node.style.margin

        self.assertEqual(node.style.margin, (0, 0, 0, 0))
        self.assertEqual(node.style.margin_top, 0)
        self.assertEqual(node.style.margin_right, 0)
        self.assertEqual(node.style.margin_bottom, 0)
        self.assertEqual(node.style.margin_left, 0)
        self.assertTrue(node.style.dirty)

    def test_set_multiple_properties(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.update(width=10, height=20)

        self.assertEqual(node.style.width, 10)
        self.assertEqual(node.style.height, 20)
        self.assertIs(node.style.top, AUTO)
        self.assertTrue(node.style.dirty)

        # Clear properties
        node.style.update(width=None, top=30)

        self.assertIs(node.style.width, AUTO)
        self.assertEqual(node.style.height, 20)
        self.assertEqual(node.style.top, 30)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Setting a non-property
        with self.assertRaises(NameError):
            node.style.update(not_a_property=10)

        self.assertFalse(node.style.dirty)

    def test_other_property_valid(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(AUTO, None), initial=OtherProperty('other_prop'))
            other_prop = validated_property('other_prop', choices=Choices(0, AUTO), initial=AUTO)

        obj = MyObject()
        self.assertEqual(obj.prop, AUTO)
        self.assertEqual(obj.prop, obj.other_prop)

        obj.other_prop = 0
        self.assertEqual(obj.prop, 0)
        self.assertEqual(obj.prop, obj.other_prop)

        obj.prop = None
        self.assertEqual(obj.prop, None)
        self.assertNotEqual(obj.prop, obj.other_prop)

    def test_other_property_invalid_no_name_argument(self):
        with self.assertRaises(TypeError):
            OtherProperty()

    def test_other_property_invalid_incorrect_property_name(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(AUTO, None), initial=OtherProperty('foobar'))

        obj = MyObject()
        with self.assertRaises(ValueError):
            obj.prop

    def test_other_property_callable_valid(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        # Check initial value LTR
        self.assertEqual(node.style.text_align, LEFT)

        # Change direction to RTL
        node.style.update(direction=RTL)
        self.assertEqual(node.style.text_align, RIGHT)

    def test_other_property_callable_invalid_no_value_method(self):
        with self.assertRaises(ValueError):
            class MyObject:
                prop = validated_property('prop', choices=Choices(AUTO, None), initial=object())

    def test_str(self):
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.update(
            width=10,
            height=20,
            margin=(30, 40, 50, 60),
            display=BLOCK
        )

        self.assertEqual(
            str(node.style),
            "display: block; height: 20px; "
            "margin-bottom: 50px; margin-left: 60px; "
            "margin-right: 40px; margin-top: 30px; width: 10px"
        )

    def test_dict(self):
        "Style declarations expose a dict-like interface"
        node = TestNode(style=CSS())
        node.layout.dirty = None

        node.style.update(
            width=10,
            height=20,
            margin=(30, 40, 50, 60),
            display=BLOCK
        )

        self.assertEqual(
            node.style.keys(),
            {'display', 'height', 'margin_bottom', 'margin_left', 'margin_right', 'margin_top', 'width'}
        )
        self.assertEqual(
            sorted(node.style.items()),
            sorted([
                ('display', BLOCK),
                ('height', 20),
                ('margin_bottom', 50),
                ('margin_left', 60),
                ('margin_right', 40),
                ('margin_top', 30),
                ('width', 10),
            ])
        )

        # A property can be set, retrieved and cleared using the CSS attribute name
        node.style['margin-bottom'] = 10
        self.assertEqual(node.style['margin-bottom'], 10)
        del node.style['margin-bottom']
        self.assertEqual(node.style['margin-bottom'], 0)

        # A property can be set, retrieved and cleared using the Python attribute name
        node.style['margin_bottom'] = 10
        self.assertEqual(node.style['margin_bottom'], 10)
        del node.style['margin_bottom']
        self.assertEqual(node.style['margin_bottom'], 0)

        # Clearing a valid property isn't an error
        del node.style['margin_bottom']
        self.assertEqual(node.style['margin_bottom'], 0)

        # Non-existent properties raise KeyError
        with self.assertRaises(KeyError):
            node.style['no-such-property'] = 'no-such-value'

        with self.assertRaises(KeyError):
            node.style['no-such-property']

        with self.assertRaises(KeyError):
            del node.style['no-such-property']
