public interface WrongInterface { }
public static class Lookup { public const int wrongLookup = 1; }
public sealed class Bad
{
    private int WrongInstance;
    private static int WrongStatic;
    private const int WrongConstant = 1;
    public int wrongProperty => WrongInstance + WrongStatic + WrongConstant + Lookup.wrongLookup;
}
