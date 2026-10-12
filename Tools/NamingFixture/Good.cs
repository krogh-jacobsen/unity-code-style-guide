public interface IFixture { }
public static class Lookup { public const int Value = 1; }
public sealed class Good
{
    private int m_value;
    private static int s_value;
    private const int k_value = 1;
    public int Value => m_value + s_value + k_value + Lookup.Value;
}
